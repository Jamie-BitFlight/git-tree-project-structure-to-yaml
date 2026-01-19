#!/usr/bin/env python3.12
"""Git Directory Structure to YAML or Tree Output Generator.

This module provides functionality similar to the 'tree' command on Linux or the Get-Tree cmdlet on Windows,
but specifically designed for Git repositories. It generates either YAML or compact text representations
of a Git repository's directory structure using GitPython and nutree.

The tool can include staged files, working directory files, and untracked files, with options to exclude
specific patterns and filter by directories.

Typical usage examples:

    # Generate YAML to stdout, with staged, working directory, and untracked files
    git-tree-project-structure-to-yaml /path/to/repo

    # Generate YAML to file
    git-tree-project-structure-to-yaml /path/to/repo --output structure.yaml

    # Generate tree output
    git-tree-project-structure-to-yaml /path/to/repo --format tree --output structure.txt

    # Exclude specific patterns
    git-tree-project-structure-to-yaml /path/to/repo --exclude node_modules --exclude .venv

Attributes:
    app: Typer application instance for CLI functionality
    logger: Module logger for diagnostic information
"""

from __future__ import annotations

import logging
import sys
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, TypeVar

import typer
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from nutree import Node, Tree

# --------------------------------------------------
# App / logging setup
# --------------------------------------------------

app = typer.Typer(pretty_exceptions_enable=True, help="Generate YAML or compact text from a Git repository")
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Enums & constants
# --------------------------------------------------


class IndentType(StrEnum):
    """Enumeration of indentation types for code formatting.

    Attributes:
        SPACES: Use spaces for indentation (default)
        TABS: Use tab characters for indentation
    """

    SPACES = auto()
    TABS = auto()


class OutputFormat(StrEnum):
    """Output format options.

    Attributes:
        YAML: Generate YAML-formatted output
        TREE: Generate tree-formatted output (similar to Unix tree command)
    """

    YAML = auto()
    TREE = auto()


# --------------------------------------------------
# Small helpers (rewritten for 3.12 clarity)
# --------------------------------------------------


def path_node_formatter(node: Node[Path]) -> str:
    """Format a Path node for display in the tree format output.

    Formats the node name for display, adding a trailing slash to directories
    to visually distinguish them from files.

    Args:
        node: Node containing a Path object

    Returns:
        str: Formatted string with appropriate directory indicator (trailing slash for directories)
    """
    path = node.data
    display_name = path.absolute().name if not path.name else path.name

    # Add trailing slash for directories
    return f"{display_name}/" if path.is_dir() else display_name


def git_lsfiles_to_path_list(repo: Repo, *args: str) -> list[Path]:
    """Convert Git ls-files output to a list of Path objects.

    Executes the git ls-files command with the provided arguments and converts
    the output into a list of absolute Path objects relative to the repository root.

    Args:
        repo: GitPython Repo object representing the Git repository
        *args: Additional arguments to pass to git ls-files command

    Returns:
        list[Path]: List of Path objects representing files in the repository

    Raises:
        typer.Exit: If the Git command fails for any reason
    """
    root_path = Path(repo.git_dir).parent
    try:
        return [root_path / line.rsplit("\t", 1)[-1] for line in repo.git.ls_files(*args).splitlines()]
    except Exception as e:
        typer.echo(f"Git command failed: {e}", err=True)
        raise typer.Exit(code=1) from e


def add_path_to_tree(tree: Tree[Path], path: Path, root: Path) -> None:
    """Add *path* to *tree* without duplicating existing nodes.

    Important: ``next(gen, default)`` evaluates *default* eagerly, so we must
    **not** pass ``cursor_node.add`` as that default or we risk creating the
    node even when it already exists. Instead we search, then add only if
    nothing was found.
    """
    # Get or create the root node representing *root*
    root_node = next((n for n in tree.children if n.data == root), None)
    if root_node is None:
        root_node = tree.add(root)

    cursor_node = root_node
    cursor_path = root

    for part in path.relative_to(root).parts:
        cursor_path /= part
        child = next((n for n in cursor_node.children if n.data == cursor_path), None)
        if child is None:
            child = cursor_node.add(cursor_path)
        cursor_node = child


def build_tree_from_git(
    repo: Repo,
    root_node: Path,
    directories: set[Path],
    exclude: set[str] | None = None,
    others: bool = True,
    stage: bool = True,
    cached: bool = False,
    exclude_standard: bool = True,
) -> Tree[Path]:
    """Build a tree structure from Git repository using GitPython and nutree.

    Creates a hierarchical tree representation of files and directories in a Git repository,
    with filtering options for different Git file states (staged, cached, untracked) and
    pattern exclusions.

    Args:
        repo: GitPython Repo object representing the Git repository
        root_node: Path object representing the root directory for the tree
        directories: Set of Path objects representing specific directories to include
        exclude: Optional set of patterns to exclude from the tree
        others: Whether to include untracked files in the output (default: True)
        stage: Whether to include staged files in the output (default: True)
        cached: Whether to include cached files in the output (default: False)
        exclude_standard: Whether to use standard Git exclusions (default: True)

    Returns:
        Tree[Path]: Tree object representing the repository structure
    """
    # Initialize exclude set if not provided
    if exclude is None:
        exclude = set()

    git_root_path = Path(repo.git_dir).parent
    logger.debug("Git root path: %s", git_root_path)
    logger.debug("Root node: %s", root_node)

    relative_root = git_root_path.relative_to(root_node)
    if relative_root == Path():
        relative_root = relative_root.absolute()
    root_dir_name = relative_root.name

    # Create a basic tree
    tree: Tree[Path] = Tree(f"# Directory Tree for {root_dir_name}")

    for directory in directories:
        tree.add(directory.absolute())

        # Prepare Git command arguments based on options
        ls_files_args: list[str] = []

        # By default with no options, git ls-files shows cached/tracked files
        # Add specific file type options if requested
        if others:
            # --others shows untracked files
            ls_files_args.append("--others")
        if stage:
            # --stage shows staged content's object name
            ls_files_args.append("--stage")
        if cached:
            # --cached explicitly shows cached/tracked files
            ls_files_args.append("--cached")
        if exclude_standard:
            # Apply standard exclusions like .gitignore patterns
            ls_files_args.append("--exclude-standard")
        for exclude_pattern in exclude:
            ls_files_args.append(f"--exclude={exclude_pattern}")
        # Only include recursive submodules if not using --others
        # (they can't be used together)
        if not others:
            ls_files_args.append("--recurse-submodules")
        ls_files_args.append(str(directory))
        # Get files in the repository using GitPython
        file_list = git_lsfiles_to_path_list(repo, *ls_files_args)
        with tree:
            # Process each file path
            for file_path in file_list:
                # Debug the path we're processing
                logger.debug("Processing %s: %s", "directory" if file_path.is_dir() else "file", file_path)
                add_path_to_tree(tree, file_path, git_root_path)
    return tree


def generate_tree_structure(tree: Tree[Path]) -> str:
    """Generate a text representation of the directory structure similar to the Unix 'tree' command.

    Creates a formatted string representation of the tree structure with ASCII/Unicode
    branch characters, similar to the output of the Unix 'tree' command. Files and
    directories are visually distinguished with appropriate formatting.

    Args:
        tree: Tree object representing the repository structure

    Returns:
        str: String containing the tree representation with ASCII/Unicode branch characters
    """
    # Leverage nutree's built-in formatting with custom node representation
    return tree.format(
        style="lines32",  # Standard tree lines style
        repr=path_node_formatter,  # Custom formatter for Path objects
        title=False,  # Don't show the tree title in the output directly
    )


def indent_string(
    string: str, indent_count: int = 0, indent_width: int = 2, indent_type: IndentType = IndentType.SPACES,
) -> str:
    """Indent a string with a specified number of spaces or tabs.

    Adds indentation to the beginning of a string using either spaces or tabs,
    based on the specified indentation type and count.

    Args:
        string: The string to indent
        indent_count: Number of indentation units to add (default: 0)
        indent_width: Width of each indentation unit in spaces (default: 2)
        indent_type: Type of indentation to use (default: IndentType.SPACES)

    Returns:
        str: The indented string
    """
    if indent_count == 0:
        return ""
    indent = " " * indent_width if indent_type == IndentType.SPACES else "\t"
    return f"{indent * indent_count}{string}"


def node_depth(node: Node[Path]) -> int:
    """Calculate the depth of a node in the tree hierarchy.

    Counts the number of parent nodes between the given node and the root.
    The root node has a depth of 0, its children have a depth of 1, etc.

    Args:
        node: The tree node to calculate depth for

    Returns:
        int: The depth of the node in the tree (0 for root)
    """
    d = 0
    current_parent: Node[Path] | None = node.parent
    while current_parent:
        current_parent = current_parent.parent
        d += 1
    return d


def get_suffix(node: Node[Path]) -> str:
    """Get the appropriate suffix for a node based on its type.

    Adds a colon suffix to directory nodes for proper YAML formatting.

    Args:
        node: The tree node to get a suffix for

    Returns:
        str: The suffix string (":" for directories, "" for files)
    """
    # Add colon for directories
    return ":" if node.data.is_dir() else ""


def yaml_formatter(node: Node[Path]) -> str:
    """Format a node for YAML output with proper indentation and type indicators.

    Combines the node name, prefix (indentation), and suffix (type indicator)
    to create a properly formatted YAML line for the node.

    Args:
        node: The tree node to format

    Returns:
        str: Formatted YAML line for the node
    """
    # Get the node name using the existing formatter for all nodes
    name = path_node_formatter(node)
    prefix = get_prefix(node)

    # Add colon for directories
    suffix = get_suffix(node)

    return f"{prefix}{name}{suffix}"


def get_prefix(node: Node[Path], indent_width: int = 2, indent_type: IndentType = IndentType.SPACES) -> str:
    """Get the appropriate prefix (indentation) for a node based on its depth in the tree.

    Calculates the indentation level based on the node's depth in the tree
    and returns the appropriate prefix string with a dash and space.

    Args:
        node: The tree node to get a prefix for
        indent_width: Width of each indentation unit in spaces (default: 2)
        indent_type: Type of indentation to use (default: IndentType.SPACES)

    Returns:
        str: The prefix string with appropriate indentation and dash
    """
    depth = node_depth(node)
    return indent_string("- ", depth, indent_width, indent_type)


def generate_yaml_output(tree: Tree[Path]) -> str:
    """Generate YAML output from the tree structure using nutree's native formatter.

    Creates a YAML representation of the tree structure, with proper indentation
    and formatting to represent the hierarchical structure of files and directories.
    The output follows standard YAML conventions with appropriate indentation.

    Args:
        tree: Tree object representing the repository structure

    Returns:
        str: String containing YAML representation of the tree
    """
    return tree.format(
        repr=yaml_formatter,  # Use our custom formatter
        title=False,  # Don't include tree title
        style="list",  # Simple list style without connectors
    )


def validate_and_return_repo(path: Path) -> Repo:
    """Validate a path as a Git repository and return the Repo object.

    Attempts to create a GitPython Repo object from the given path,
    searching parent directories if necessary. Exits with an error
    if the path is not a valid Git repository or does not exist.

    Args:
        path: Path to validate as a Git repository

    Returns:
        Repo: GitPython Repo object for the repository

    Raises:
        typer.Exit: If the path is not a valid Git repository or does not exist
    """
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        logger.exception("Error: Path '%s' is not a valid Git repository: %s", path, e)
        raise typer.Exit(code=1) from e
    except NoSuchPathError as e:
        logger.exception("Error: Path '%s' does not exist: %s", path, e)
        raise typer.Exit(code=1) from e


def validate_and_return_path(path: Path) -> Path:
    """Validate that a path exists and return its resolved form.

    Attempts to resolve the given path and verify that it exists on the filesystem.
    Exits with an error if the path does not exist.

    Args:
        path: Path to validate and resolve

    Returns:
        Path: Resolved Path object if valid

    Raises:
        typer.Exit: If the path does not exist
    """
    try:
        return Path(path).resolve(strict=True)
    except FileNotFoundError as e:
        logger.exception("Error: Path '%s' does not exist", path)
        raise typer.Exit(code=1) from e


T = TypeVar("T")


def empty_list_if_none[T](value: list[T] | None) -> list[T]:
    """Return an empty list if the input value is None, otherwise return the input value.

    A utility function to safely handle potentially None list values by returning
    an empty list instead, avoiding NoneType errors in subsequent operations.

    Args:
        value: A list or None

    Returns:
        list[T]: The original list if not None, otherwise an empty list
    """
    return value or []


@app.command()
def main(
    repo_paths: Annotated[list[Path] | None, typer.Argument(help="Paths to directories in the Git repository")] = None,
    repo_path: Annotated[
        Path | None,
        typer.Option(
            "--repo",
            help="Path to the Git repository root. Defaults to current directory if not specified.",
            show_default=False,
        ),
    ] = None,
    output: Annotated[
        Path | None, typer.Option("-o", "--output", help="Output file (default: print to stdout)"),
    ] = None,
    format: Annotated[OutputFormat, typer.Option("-f", "--format", help="Output format")] = OutputFormat.YAML,
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Enable verbose output")] = False,
    exclude: Annotated[
        list[str] | None, typer.Option("-x", "--exclude", help="Patterns to exclude (can be used multiple times)"),
    ] = None,
    others: Annotated[bool, typer.Option("--others", help="Show untracked files in the output")] = True,
    stage: Annotated[bool, typer.Option("--stage", help="Show staged files in the output")] = True,
    cached: Annotated[bool, typer.Option("--cached", help="Show cached/tracked files in the output")] = False,
    exclude_standard: Annotated[bool, typer.Option("--exclude-standard", help="Use standard Git exclusions")] = True,
    repo_as_root: Annotated[
        bool, typer.Option("--repo-as-root", help="Use the repository root as the root directory"),
    ] = True,
) -> None:
    """Generate YAML or compact text from Git repository structure.

    Main entry point for the CLI application. Processes command-line arguments,
    validates inputs, builds a tree representation of the Git repository structure,
    and outputs the result in the requested format.

    Args:
        repo_paths: List of paths to directories within the Git repository to include
        repo_path: Path to the Git repository (defaults to current directory)
        output: Output file path (defaults to stdout)
        format: Output format (yaml or tree)
        exclude: List of patterns to exclude from the output
        others: Whether to include untracked files in the output
        stage: Whether to include staged files in the output
        cached: Whether to include cached files in the output
        exclude_standard: Whether to use standard Git exclusions
        verbose: Whether to enable verbose output
        repo_as_root: Whether to use the repository root as the root directory

    Returns:
        None

    Raises:
        typer.Exit: If any validation fails or an error occurs during processing
    """
    # Configure logging level and direct all logs to stderr
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr,
    )
    current_dir = Path.cwd()

    base_repo_path = validate_and_return_path(current_dir if repo_path is None else repo_path)

    git_repository = validate_and_return_repo(base_repo_path)

    root_node = Path(Path(git_repository.git_dir).parent if repo_as_root else base_repo_path)
    repo_as_root = root_node == base_repo_path

    repo_paths = empty_list_if_none(repo_paths)
    logger.debug("Repository paths: %s", repo_paths)
    logger.debug("Root node for relativity: %s", root_node)

    # Safely convert paths to relative
    relative_repo_paths = set()
    if not repo_paths:
        relative_repo_paths = {root_node}
        logger.debug("No repo paths provided, using root node: %s", root_node)
    else:
        for path in repo_paths:
            path_obj = Path(path)
            logger.debug("Processing path: %s", path_obj)
            try:
                rel_path = path_obj.relative_to(root_node)
                logger.debug("Successfully made relative: %s", rel_path)
                relative_repo_paths.add(rel_path)
            except ValueError as e:
                logger.exception("Error making path relative: %s - %s", path_obj, e)
                # You could either skip this path or use a different approach
                # For debugging, we'll try to continue with the original path
                logger.debug("Using original path instead: %s", path_obj)
                relative_repo_paths.add(path_obj)

    logger.debug("Final relative repo paths: %s", relative_repo_paths)
    for repo_path in relative_repo_paths:
        if not repo_path.is_dir():
            logger.error("Error: Path '%s' is not a directory", repo_path)
            raise typer.Exit(code=1)

    # Convert exclude list to a set for faster lookups
    exclude_set = set(empty_list_if_none(exclude))
    options_set = set()
    if others:
        options_set.add("--others")
    if stage:
        options_set.add("--stage")
    if cached:
        options_set.add("--cached")
    if exclude_standard:
        options_set.add("--exclude-standard")

    try:
        # Convert directories to relative paths within the repository if provided

        logger.debug("Using paths: %s", relative_repo_paths)
        logger.debug("Using options: %s", options_set)

        # Build a tree from the Git repository using GitPython and nutree
        tree = build_tree_from_git(
            repo=git_repository,
            root_node=root_node,
            directories=relative_repo_paths,
            exclude=exclude_set,
            others=others,
            stage=stage,
            cached=cached,
            exclude_standard=exclude_standard,
        )

        # Generate output based on requested format
        if format == OutputFormat.YAML:
            # Generate YAML using nutree's native formatting
            yaml_content = generate_yaml_output(tree)

            if yaml_content:
                output_content = yaml_content
            else:
                # No files found but that's not an error - just show empty structure
                logger.info("No matching files found in the repository with the specified options")
                output_content = f"# Nothing found that matched the specified options: {options_set}\n"
        else:  # tree format
            # Use nutree's built-in formatting
            output_content = generate_tree_structure(tree)

        # Write to output file or print to stdout
        if output:
            with open(output, "w") as f:
                f.write(output_content)
            logger.info("Output written to %s", output)
        else:
            pass

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
