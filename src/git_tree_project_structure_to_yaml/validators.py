"""Validation functions for paths and Git repositories."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError

logger = logging.getLogger(__name__)


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


def validate_directories(paths: set[Path]) -> None:
    """Validate that all paths are directories.

    Args:
        paths: Set of paths to validate

    Raises:
        typer.Exit: If any path is not a directory
    """
    for path in paths:
        if not path.is_dir():
            logger.error("Error: Path '%s' is not a directory", path)
            raise typer.Exit(code=1)
