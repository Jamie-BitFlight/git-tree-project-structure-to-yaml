#!/usr/bin/env python3.12
"""
Git Directory Structure to YAML or Tree Output Generator

This works like the 'tree' command on linux, or the Get-Tree cmdlet on Windows.

This script generates a YAML or compact text representation of a Git repository's
directory structure using GitPython and nutree.

Examples:
    # Generate YAML to Stdio, with the staged files, the working directory files and the untracked files
    git-tree-structure /path/to/repo

    # Generate YAML to file, with the staged files, the working directory files and the untracked files
    git-tree-structure /path/to/repo --output structure.yaml

    # Generate tree output
    git-tree-structure /path/to/repo --format tree --output structure.txt

    # Exclude specific patterns
    git-tree-structure /path/to/repo --exclude node_modules --exclude .venv
"""

from __future__ import annotations

import logging
import sys
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Iterator

import typer
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from nutree import Node, Tree

# Create the Typer app with help text
app = typer.Typer(pretty_exceptions_enable=False, help="Generate YAML or compact text from Git repository structure")

# Setup logger
logger = logging.getLogger(__name__)


class IndentType(StrEnum):
    SPACES = auto()
    TABS = auto()


class OutputFormat(StrEnum):
    """Output format options."""

    YAML = auto()
    TREE = auto()


def path_node_formatter(node: Node[Path]) -> str:
    """
    Format a Path node for display in the tree format output.

    Args:
        node: Node containing a Path object

    Returns:
        Formatted string with appropriate directory indicator
    """
    path = node.data
    display_name = path.absolute().name

    # Add trailing slash for directories
    return f"{display_name}/" if path.is_dir() else display_name


def git_lsfiles_to_path_list(repo: Repo, *args: str) -> list[Path]:
    try:
        root_path = Path(repo.git_dir).parent
        paths = [root_path / line.split("\t")[-1] for line in repo.git.ls_files(*args).splitlines()]
        logger.debug("Found %d paths", len(paths))
        return paths
    except Exception as e:
        logger.error("Git command failed: %s", e)
        raise typer.Exit(code=1) from e


def add_path_to_tree(tree: Tree[Path], path: Path, root_path: Path) -> None:
    # Split path into parts
    parts = path.relative_to(root_path).parts

    if not parts:  # Empty path
        return

    # Start at the root node
    current_node = tree.first_child()
    if not current_node:
        logger.debug("Creating root node in tree")
        current_node = tree.add(root_path)
    current_path = root_path

    # Efficiently traverse/build the path
    for part in parts:
        next_path = current_path / part

        # Find existing node or create new one
        existing_nodes = [node for node in current_node.children if node.data == next_path]
        current_node = existing_nodes[0] if existing_nodes else current_node.add(next_path)

        current_path = next_path

    logger.debug("Added path to tree: %s", path)


def build_tree_from_git(
    repo: Repo,
    root_node: Path,
    directories: set[Path],
    exclude: set[str] | None = None,
    others: bool = True,
    stage: bool = True,
    cached: bool = False,
    exclude_standard: bool = True,
) -> Tree:
    """
    Build a tree structure from Git repository using GitPython and nutree.

    Args:
        repo_path: Path to the Git repository
        exclude: Optional set of patterns to exclude
        others: Include untracked files in the output
        stage: Include staged files in the output
        cached: Include cached files in the output
        exclude_standard: Use standard Git exclusions
        directories: Optional specific directories to include

    Returns:
        Tree object representing the repository structure
    """
    # Initialize exclude set if not provided
    if exclude is None:
        exclude = set()

    git_root_path = Path(repo.git_dir).parent
    logger.debug("Git root path: %s", git_root_path)
    logger.debug("Root node: %s", root_node)

    relative_root = git_root_path.relative_to(root_node)
    if relative_root == Path("."):
        relative_root = relative_root.absolute()
    root_dir_name = relative_root.name

    # Create a basic tree
    tree: Tree[Path] = Tree(f"# Directory Tree for {root_dir_name}")

    for directory in directories:
        tree.add(directory.relative_to(git_root_path))

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
    """
    Generate a text representation of the directory structure similar to the Unix 'tree' command.

    Args:
        tree: Tree object representing the repository structure

    Returns:
        String containing the tree representation with ASCII/Unicode branch characters
    """
    # Leverage nutree's built-in formatting with custom node representation
    return tree.format(
        style="lines32",  # Standard tree lines style
        repr=path_node_formatter,  # Custom formatter for Path objects
        title=False,  # Don't show the tree title in the output directly
    )

def indent_string(string: str, indent_count: int = 0, indent_width: int = 2, indent_type: IndentType = IndentType.SPACES) -> str:
    indent_unit = " " * indent_width if indent_type == IndentType.SPACES else "\t"
    return f"{indent_unit * indent_count}{string}"
    
def generate_yaml_output(tree: Tree[Path]) -> str:
    """
    Generate YAML output from the tree structure using nutree's native formatter.

    Args:
        tree: Tree object representing the repository structure

    Returns:
        String containing YAML representation of the tree
    """
    # Check if tree has any content
    first_child = tree.first_child()
    if first_child is None or not hasattr(first_child, "children") or not first_child.children:
        logger.debug("No files in tree structure")
        return ""

    def _get_suffix(node: Node[Path]) -> str:
        return ":" if node.data.is_dir() else ""

    def _get_prefix(node: Node[Path], indent_width: int = 2, indent_type: IndentType = IndentType.SPACES) -> str:
        if node.parent is None:
            return ""
        
        def _iter_parent(node: Node[Path]) -> Iterator[Node[Path]]:
            while node.parent:
                yield node.parent
                node = node.parent
        # Calculate depth by traversing parent chain
        # Using a generator expression with sum() is more efficient than manual counting
        depth = sum(True for _ in _iter_parent(node))
        return indent_string("- ", depth, indent_width, indent_type)

    # Define a custom YAML formatter function that uses our existing formatter
    def yaml_formatter(node: Node[Path]) -> str:
        # Get the node name using the existing formatter for all nodes
        name = path_node_formatter(node)
        prefix = _get_prefix(node)

        # Add colon for directories
        suffix = _get_suffix(node)

        return f"{prefix}{name}{suffix}"

    # Use nutree's built-in formatter with our custom node formatter
    # The 'list' style gives a flat list structure without connectors
    yaml_output = tree.format(
        repr=yaml_formatter,  # Use our custom formatter
        title=False,  # Don't include tree title
        style="list",  # Simple list style without connectors
    )

    logger.debug("Generated YAML output: %s...", yaml_output[:100] if len(yaml_output) > 100 else yaml_output)
    return yaml_output


def validate_and_return_repo(path: Path) -> Repo:
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        logger.error("Error: Path '%s' is not a valid Git repository", path)
        raise typer.Exit(code=1) from None
    except NoSuchPathError:
        logger.error("Error: Path '%s' does not exist", path)
        raise typer.Exit(code=1) from None


def validate_and_return_path(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=True)
    except FileNotFoundError:
        logger.error("Error: Path '%s' does not exist", path)
        raise typer.Exit(code=1) from None


def empty_list_if_none[T](value: list[T] | None) -> list[T]:
    return value if value is not None else []


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
        Path | None, typer.Option("-o", "--output", help="Output file (default: print to stdout)")
    ] = None,
    format: Annotated[OutputFormat, typer.Option("-f", "--format", help="Output format")] = OutputFormat.YAML,
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Enable verbose output")] = False,
    exclude: Annotated[
        list[str] | None, typer.Option("-x", "--exclude", help="Patterns to exclude (can be used multiple times)")
    ] = None,
    others: Annotated[bool, typer.Option("--others", help="Show untracked files in the output")] = True,
    stage: Annotated[bool, typer.Option("--stage", help="Show staged files in the output")] = True,
    cached: Annotated[bool, typer.Option("--cached", help="Show cached/tracked files in the output")] = False,
    exclude_standard: Annotated[bool, typer.Option("--exclude-standard", help="Use standard Git exclusions")] = True,
    repo_as_root: Annotated[
        bool, typer.Option("--repo-as-root", help="Use the repository root as the root directory")
    ] = True,
) -> None:
    """Generate YAML or compact text from Git repository structure."""
    # Configure logging level and direct all logs to stderr
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr
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
                logger.error("Error making path relative: %s - %s", path_obj, e)
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
            print(output_content)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
