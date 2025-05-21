from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from nutree import Tree

from git_tree_project_structure_to_yaml._cli import generate_yaml_output, path_node_formatter


@pytest.fixture
def mock_path_is_dir():
    """Fixture that allows mocking Path.is_dir() method in tests."""

    def _mock_factory(dir_names: set[str]):
        """Create a mock is_dir method that identifies specific paths as directories."""

        def _mock_is_dir(self):
            return self.name in dir_names

        return _mock_is_dir

    return _mock_factory


def verify_yaml_output(result: str) -> dict[str, Any] | None:
    """Verify a string is valid YAML and return the parsed result."""
    try:
        parsed_yaml = yaml.safe_load(result)
        assert parsed_yaml is not None, "YAML should parse to a valid structure"
        assert isinstance(parsed_yaml, dict), "Root should be a dictionary"
        return parsed_yaml
    except yaml.YAMLError as e:
        pytest.fail(f"Invalid YAML format: {e}")
        return None


def get_indentation_level(line: str) -> int:
    """Get the indentation level of a line by counting leading whitespace."""
    return len(line) - len(line.lstrip())


class TestPathNodeFormatter:
    def test_format_file(self):
        """Test formatting a file node (no trailing slash)."""
        # Create a node with a Path object representing a file
        tree = Tree("Test Tree")
        node = tree.add(Path("test_file.txt"))

        # Format the node and verify it doesn't have a trailing slash
        result = path_node_formatter(node)
        assert result == "test_file.txt"

    def test_format_directory(self, mock_path_is_dir):
        """Test formatting a directory node (with trailing slash)."""
        with pytest.MonkeyPatch.context() as mp:
            # Use fixture to mock Path.is_dir to identify our test path as a directory
            mock_is_dir = mock_path_is_dir({"test_dir"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            # Create a node with a Path object representing a directory
            tree = Tree("Test Tree")
            node = tree.add(Path("test_dir"))

            # Format the node and verify it has a trailing slash
            result = path_node_formatter(node)
            assert result == "test_dir/"


class TestGenerateYamlOutput:
    def test_basic_yaml_conversion(self, mock_path_is_dir):
        """Test basic tree to YAML conversion with properly mocked file paths."""
        # Create a temp directory for proper Path objects with is_dir() behavior
        with pytest.MonkeyPatch.context() as mp:
            # Mock the is_dir method to return True for directories and False for files
            mock_is_dir = mock_path_is_dir({"root", "dir1"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            # Create a tree with paths that will have proper is_dir behavior
            tree = Tree[Path]("Test Tree")
            root = tree.add(Path("root"))  # Will be treated as a directory
            root.add(Path("file1.txt"))  # Will be treated as a file
            root.add(Path("file2.md"))  # Will be treated as a file

            # Convert to YAML string
            result = generate_yaml_output(tree)

            # Print actual result for debugging
            print(f"\nGenerated YAML output: {result!r}")
            print(f"Lines: {list(result.strip().split('\n'))}")

            # Verify basic content presence
            assert isinstance(result, str)
            assert "root" in result, "Root node missing"
            assert "file1.txt" in result, "file1.txt missing"
            assert "file2.md" in result, "file2.md missing"

            # Verify and parse YAML
            parsed_yaml = verify_yaml_output(result)
            if parsed_yaml:
                # Extract and verify structure
                root_key = next(iter(parsed_yaml))
                assert "root" in root_key, f"Expected 'root' in root key, got {root_key!r}"

                # Check for files in the YAML structure
                files = str(parsed_yaml[root_key])
                assert "file1.txt" in files, "file1.txt missing from parsed YAML"
                assert "file2.md" in files, "file2.md missing from parsed YAML"

            # Check proper indentation structure in the output
            lines = [line.rstrip() for line in result.strip().split("\n")]

            # Find root line and file lines
            root_line = next((line for line in lines if "root" in line), None)
            file_lines = [line for line in lines if "file1" in line or "file2" in line]

            # Verify proper indentation structure
            assert root_line is not None, "Root line missing"
            assert file_lines, "File lines missing"

            # Files should be indented more than root
            root_indent = len(root_line) - len(root_line.lstrip())
            for file_line in file_lines:
                file_indent = len(file_line) - len(file_line.lstrip())
                assert file_indent > root_indent, f"File {file_line} not properly indented relative to root"

    def test_nested_yaml_structure(self, mock_path_is_dir):
        """Test conversion of nested structures to YAML."""
        # Create a tree with nested structure using mocked Path objects
        with pytest.MonkeyPatch.context() as mp:
            # Mock is_dir to identify directories correctly
            mock_is_dir = mock_path_is_dir({"root", "dir1", "level1", "level2", "level3"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            # Create tree with nested structure
            tree = Tree[Path]("Test Tree")
            root = tree.add(Path("root"))  # Directory
            dir1 = root.add(Path("dir1"))  # Directory
            dir1.add(Path("nested1.txt"))  # File
            dir1.add(Path("nested2.txt"))  # File

            # Convert to YAML string
            result = generate_yaml_output(tree)
            print("\nNested structure output:")
            print(repr(result))

            # Verify we have valid YAML output
            parsed_yaml = verify_yaml_output(result)
            if parsed_yaml:
                # Get root key and verify it exists
                root_key = next(iter(parsed_yaml))
                root_value = parsed_yaml[root_key]

                # Verify hierarchy - dir1 should be a child of root with nested files
                assert "dir1" in str(root_value), "dir1 directory missing from structure"
                assert "nested1.txt" in str(root_value), "nested1.txt missing from structure"
                assert "nested2.txt" in str(root_value), "nested2.txt missing from structure"

            # Verify proper indentation structure
            lines = [line.rstrip() for line in result.strip().split("\n")]

            # Root line should come first, followed by dir1 and nested files
            root_idx = next((i for i, line in enumerate(lines) if "root" in line), None)
            dir1_idx = next((i for i, line in enumerate(lines) if "dir1" in line), None)
            nested_indices = [i for i, line in enumerate(lines) if "nested" in line]

            # Verify all lines are present
            assert root_idx is not None, "Root line missing"
            assert dir1_idx is not None, "dir1 line missing"
            assert len(nested_indices) == 2, "Expected exactly 2 nested file entries"

            # Verify proper indentation hierarchy
            root_indent = get_indentation_level(lines[root_idx])
            dir1_indent = get_indentation_level(lines[dir1_idx])

            # dir1 should be indented more than root
            assert dir1_indent > root_indent, "dir1 not properly indented relative to root"

            # Nested files should be indented more than dir1
            for idx in nested_indices:
                nested_indent = get_indentation_level(lines[idx])
                assert nested_indent > dir1_indent, "Nested file not properly indented relative to dir1"

    def test_deep_nesting_indentation(self, mock_path_is_dir):
        """Test indentation with deeply nested directories."""
        with pytest.MonkeyPatch.context() as mp:
            # Mock is_dir to identify directories correctly
            mock_is_dir = mock_path_is_dir({"root", "level1", "level2", "level3"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            # Create a tree with multiple levels of nesting
            tree = Tree[Path]("Test Tree")
            root = tree.add(Path("root"))  # Directory
            level1 = root.add(Path("level1"))  # Directory
            level2 = level1.add(Path("level2"))  # Directory
            level3 = level2.add(Path("level3"))  # Directory
            level3.add(Path("deep_file.txt"))  # File

            # Convert to YAML string
            result = generate_yaml_output(tree)
            print("\nDeep nesting output:")
            print(result)

            # Verify the output is valid YAML
            verify_yaml_output(result)

            # Verify the nested structure
            lines = [line.rstrip() for line in result.strip().split("\n")]

            # Get indentation levels
            indentation_levels = {}
            for name in ["root", "level1", "level2", "level3", "deep_file"]:
                line = next((line for line in lines if name in line), None)
                assert line is not None, f"{name} missing from output"
                indentation_levels[name] = get_indentation_level(line)

            # Verify increasing indentation with depth
            assert indentation_levels["level1"] > indentation_levels["root"], "level1 should be indented more than root"
            assert indentation_levels["level2"] > indentation_levels["level1"], (
                "level2 should be indented more than level1"
            )
            assert indentation_levels["level3"] > indentation_levels["level2"], (
                "level3 should be indented more than level2"
            )
            assert indentation_levels["deep_file"] > indentation_levels["level3"], (
                "deep_file should be indented more than level3"
            )

    def test_empty_tree_conversion(self):
        """Test conversion of an empty tree."""
        # Create an empty tree
        tree = Tree[Path]("Empty Tree")

        # Convert to YAML format
        result = generate_yaml_output(tree)

        # Verify empty result
        assert result == ""
