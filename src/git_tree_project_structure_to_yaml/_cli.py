#!/usr/bin/env python3.12
"""Git Directory Structure to YAML or Tree Output Generator.

This module provides functionality similar to the 'tree' command on Linux or the Get-Tree cmdlet on Windows,
but specifically designed for Git repositories. It generates either YAML or compact text representations
of a Git repository's directory structure using GitPython and nutree.

Typical usage examples:

    # Generate YAML to stdout, with staged, working directory, and untracked files
    git-tree-project-structure-to-yaml /path/to/repo

    # Generate YAML to file
    git-tree-project-structure-to-yaml /path/to/repo --output structure.yaml

    # Generate tree output
    git-tree-project-structure-to-yaml /path/to/repo --format tree --output structure.txt

    # Exclude specific patterns
    git-tree-project-structure-to-yaml /path/to/repo --exclude node_modules --exclude .venv
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Annotated

import typer

from .tree import build_tree_from_git
from .types import OutputFormat
from .utils import empty_list_if_none, generate_output_content, resolve_repo_paths
from .validators import validate_and_return_path, validate_and_return_repo, validate_directories

app = typer.Typer(pretty_exceptions_enable=True, help="Generate YAML or compact text from a Git repository")
logger = logging.getLogger(__name__)


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
    output_format: Annotated[OutputFormat, typer.Option("-f", "--format", help="Output format")] = OutputFormat.YAML,
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
    """Generate YAML or compact text from Git repository structure.

    Main entry point for the CLI application. Processes command-line arguments,
    validates inputs, builds a tree representation of the Git repository structure,
    and outputs the result in the requested format.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr
    )
    current_dir = Path.cwd()

    base_repo_path = validate_and_return_path(current_dir if repo_path is None else repo_path)
    git_repository = validate_and_return_repo(base_repo_path)
    root_node = Path(Path(git_repository.git_dir).parent if repo_as_root else base_repo_path)

    repo_paths_list = empty_list_if_none(repo_paths)
    relative_repo_paths = resolve_repo_paths(repo_paths_list, root_node)
    validate_directories(relative_repo_paths)

    exclude_set = set(empty_list_if_none(exclude))
    options_set = {
        opt
        for opt, flag in [
            ("--others", others),
            ("--stage", stage),
            ("--cached", cached),
            ("--exclude-standard", exclude_standard),
        ]
        if flag
    }

    try:
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

        output_content = generate_output_content(tree, output_format, options_set)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_content)
            logger.info("Output written to %s", output)

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
