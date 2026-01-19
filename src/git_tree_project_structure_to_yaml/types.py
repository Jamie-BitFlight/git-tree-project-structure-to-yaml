"""Type definitions and enums for git-tree-project-structure-to-yaml."""

from __future__ import annotations

from enum import StrEnum, auto


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
