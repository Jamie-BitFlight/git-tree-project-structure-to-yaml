"""Output formatting functions for tree and YAML generation."""

from __future__ import annotations

from pathlib import Path

from nutree import Node, Tree

from .types import IndentType


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


def indent_string(
    string: str, indent_count: int = 0, indent_width: int = 2, indent_type: IndentType = IndentType.SPACES
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
    return ":" if node.data.is_dir() else ""


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


def yaml_formatter(node: Node[Path]) -> str:
    """Format a node for YAML output with proper indentation and type indicators.

    Combines the node name, prefix (indentation), and suffix (type indicator)
    to create a properly formatted YAML line for the node.

    Args:
        node: The tree node to format

    Returns:
        str: Formatted YAML line for the node
    """
    name = path_node_formatter(node)
    prefix = get_prefix(node)
    suffix = get_suffix(node)
    return f"{prefix}{name}{suffix}"


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
    return tree.format(style="lines32", repr=path_node_formatter, title=False)


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
    return tree.format(repr=yaml_formatter, title=False, style="list")
