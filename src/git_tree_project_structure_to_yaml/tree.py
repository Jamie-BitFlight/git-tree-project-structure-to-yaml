"""Tree building and manipulation functions for Git repositories."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from git import Repo
from nutree import Tree

logger = logging.getLogger(__name__)


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


def build_ls_files_args(
    directory: Path, exclude: set[str], others: bool, stage: bool, cached: bool, exclude_standard: bool
) -> list[str]:
    """Build arguments for git ls-files command.

    Args:
        directory: Directory to list files from
        exclude: Set of patterns to exclude
        others: Whether to include untracked files
        stage: Whether to include staged files
        cached: Whether to include cached files
        exclude_standard: Whether to use standard Git exclusions

    Returns:
        list[str]: Arguments for git ls-files command
    """
    ls_files_args: list[str] = []
    if others:
        ls_files_args.append("--others")
    if stage:
        ls_files_args.append("--stage")
    if cached:
        ls_files_args.append("--cached")
    if exclude_standard:
        ls_files_args.append("--exclude-standard")
    for exclude_pattern in exclude:
        ls_files_args.append(f"--exclude={exclude_pattern}")
    if not others:
        ls_files_args.append("--recurse-submodules")
    ls_files_args.append(str(directory))
    return ls_files_args


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
    exclude = exclude or set()
    git_root_path = Path(repo.git_dir).parent
    logger.debug("Git root path: %s", git_root_path)
    logger.debug("Root node: %s", root_node)

    relative_root = git_root_path.relative_to(root_node)
    if relative_root == Path():
        relative_root = relative_root.absolute()
    root_dir_name = relative_root.name

    tree: Tree[Path] = Tree(f"# Directory Tree for {root_dir_name}")

    for directory in directories:
        tree.add(directory.absolute())
        ls_files_args = build_ls_files_args(directory, exclude, others, stage, cached, exclude_standard)
        file_list = git_lsfiles_to_path_list(repo, *ls_files_args)
        with tree:
            for file_path in file_list:
                logger.debug("Processing %s: %s", "directory" if file_path.is_dir() else "file", file_path)
                add_path_to_tree(tree, file_path, git_root_path)
    return tree
