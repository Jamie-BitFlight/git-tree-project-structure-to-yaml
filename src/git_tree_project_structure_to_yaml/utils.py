"""Utility functions for path handling and output generation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TypeVar

from nutree import Tree

from .formatters import generate_tree_structure, generate_yaml_output
from .types import OutputFormat

logger = logging.getLogger(__name__)

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


def resolve_repo_paths(repo_paths: list[Path], root_node: Path) -> set[Path]:
    """Convert repository paths to relative paths within the root node.

    Args:
        repo_paths: List of paths to process
        root_node: Root node to make paths relative to

    Returns:
        set[Path]: Set of resolved paths
    """
    if not repo_paths:
        logger.debug("No repo paths provided, using root node: %s", root_node)
        return {root_node}

    relative_repo_paths: set[Path] = set()
    for path in repo_paths:
        path_obj = Path(path)
        logger.debug("Processing path: %s", path_obj)
        try:
            rel_path = path_obj.relative_to(root_node)
            logger.debug("Successfully made relative: %s", rel_path)
            relative_repo_paths.add(rel_path)
        except ValueError as e:
            logger.exception("Error making path relative: %s - %s", path_obj, e)
            logger.debug("Using original path instead: %s", path_obj)
            relative_repo_paths.add(path_obj)
    return relative_repo_paths


def generate_output_content(
    tree: Tree[Path], output_format: OutputFormat, options_set: set[str],
) -> str:
    """Generate output content based on the requested format.

    Args:
        tree: Tree object representing the repository structure
        output_format: Output format (yaml or tree)
        options_set: Set of options used for the message when no files found

    Returns:
        str: Generated output content
    """
    if output_format == OutputFormat.YAML:
        yaml_content = generate_yaml_output(tree)
        if yaml_content:
            return yaml_content
        logger.info("No matching files found in the repository with the specified options")
        return f"# Nothing found that matched the specified options: {options_set}\n"
    return generate_tree_structure(tree)
