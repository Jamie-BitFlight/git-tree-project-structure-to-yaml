from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest
import typer
import yaml
from nutree import Tree

from git_tree_project_structure_to_yaml._cli import (
    IndentType,
    OutputFormat,
    add_path_to_tree,
    build_ls_files_args,
    build_tree_from_git,
    empty_list_if_none,
    generate_output_content,
    generate_yaml_output,
    git_lsfiles_to_path_list,
    indent_string,
    main,
    path_node_formatter,
    resolve_repo_paths,
    validate_and_return_path,
    validate_and_return_repo,
    validate_directories,
)


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
    def test_format_file(self) -> None:
        """Test formatting a file node (no trailing slash)."""
        # Create a node with a Path object representing a file
        tree = Tree("Test Tree")
        node = tree.add(Path("test_file.txt"))

        # Format the node and verify it doesn't have a trailing slash
        result = path_node_formatter(node)
        assert result == "test_file.txt"

    def test_format_directory(self, mock_path_is_dir) -> None:
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
    def test_basic_yaml_conversion(self, mock_path_is_dir) -> None:
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

    def test_nested_yaml_structure(self, mock_path_is_dir) -> None:
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

    def test_deep_nesting_indentation(self, mock_path_is_dir) -> None:
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

    def test_empty_tree_conversion(self) -> None:
        """Test conversion of an empty tree."""
        # Create an empty tree
        tree = Tree[Path]("Empty Tree")

        # Convert to YAML format
        result = generate_yaml_output(tree)

        # Verify empty result
        assert result == ""


class TestGitLsfilesToPathList:
    """Tests for the git_lsfiles_to_path_list function."""

    def test_successful_ls_files_returns_path_list(self) -> None:
        """Test that successful git ls-files returns a list of paths."""
        mock_repo = MagicMock()
        mock_repo.git_dir = "/fake/repo/.git"
        mock_repo.git.ls_files.return_value = "file1.txt\ndir/file2.py"

        result = git_lsfiles_to_path_list(mock_repo, "--cached")

        assert len(result) == 2
        assert result[0] == Path("/fake/repo/file1.txt")
        assert result[1] == Path("/fake/repo/dir/file2.py")

    def test_ls_files_with_staged_output(self) -> None:
        """Test parsing staged output with mode/hash prefix."""
        mock_repo = MagicMock()
        mock_repo.git_dir = "/fake/repo/.git"
        # Staged output format: mode hash stage\tfilename
        mock_repo.git.ls_files.return_value = "100644 abc123 0\tfile1.txt\n100644 def456 0\tfile2.py"

        result = git_lsfiles_to_path_list(mock_repo, "--stage")

        assert len(result) == 2
        assert result[0] == Path("/fake/repo/file1.txt")
        assert result[1] == Path("/fake/repo/file2.py")

    def test_git_command_failure_raises_exit(self) -> None:
        """Test that git command failure raises typer.Exit."""
        mock_repo = MagicMock()
        mock_repo.git_dir = "/fake/repo/.git"
        mock_repo.git.ls_files.side_effect = Exception("Git command failed")

        with pytest.raises(typer.Exit) as exc_info:
            git_lsfiles_to_path_list(mock_repo, "--cached")

        assert exc_info.value.exit_code == 1


class TestAddPathToTree:
    """Tests for the add_path_to_tree function."""

    def test_add_single_file_to_tree(self, mock_path_is_dir) -> None:
        """Test adding a single file to an empty tree."""
        with pytest.MonkeyPatch.context() as mp:
            mock_is_dir = mock_path_is_dir({"root"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            tree = Tree[Path]("Test Tree")
            root = Path("/root")
            file_path = Path("/root/file.txt")

            add_path_to_tree(tree, file_path, root)

            # Verify tree has the root and file
            assert len(tree.children) == 1
            root_node = tree.children[0]
            assert root_node.data == root
            assert len(root_node.children) == 1
            assert root_node.children[0].data == file_path

    def test_add_nested_file_creates_intermediate_directories(self, mock_path_is_dir) -> None:
        """Test adding a deeply nested file creates intermediate nodes."""
        with pytest.MonkeyPatch.context() as mp:
            mock_is_dir = mock_path_is_dir({"root", "dir1", "dir2"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            tree = Tree[Path]("Test Tree")
            root = Path("/root")
            nested_file = Path("/root/dir1/dir2/file.txt")

            add_path_to_tree(tree, nested_file, root)

            # Verify tree structure
            root_node = tree.children[0]
            assert root_node.data == root
            dir1_node = root_node.children[0]
            assert dir1_node.data == Path("/root/dir1")
            dir2_node = dir1_node.children[0]
            assert dir2_node.data == Path("/root/dir1/dir2")
            file_node = dir2_node.children[0]
            assert file_node.data == nested_file

    def test_add_duplicate_path_does_not_create_duplicate(self, mock_path_is_dir) -> None:
        """Test adding the same path twice doesn't duplicate nodes."""
        with pytest.MonkeyPatch.context() as mp:
            mock_is_dir = mock_path_is_dir({"root"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            tree = Tree[Path]("Test Tree")
            root = Path("/root")
            file_path = Path("/root/file.txt")

            add_path_to_tree(tree, file_path, root)
            add_path_to_tree(tree, file_path, root)

            # Should still have only one file
            root_node = tree.children[0]
            assert len(root_node.children) == 1


class TestBuildLsFilesArgs:
    """Tests for the build_ls_files_args function."""

    def test_build_args_with_others_flag(self) -> None:
        """Test building args with --others flag."""
        args = build_ls_files_args(
            directory=Path("/test"),
            exclude=set(),
            others=True,
            stage=False,
            cached=False,
            exclude_standard=False,
        )

        assert "--others" in args
        assert "--stage" not in args
        assert "--cached" not in args
        assert "--recurse-submodules" not in args  # Not added when others=True
        assert str(Path("/test")) in args

    def test_build_args_with_stage_flag(self) -> None:
        """Test building args with --stage flag."""
        args = build_ls_files_args(
            directory=Path("/test"),
            exclude=set(),
            others=False,
            stage=True,
            cached=False,
            exclude_standard=False,
        )

        assert "--stage" in args
        assert "--others" not in args
        assert "--recurse-submodules" in args  # Added when others=False

    def test_build_args_with_cached_flag(self) -> None:
        """Test building args with --cached flag."""
        args = build_ls_files_args(
            directory=Path("/test"),
            exclude=set(),
            others=False,
            stage=False,
            cached=True,
            exclude_standard=False,
        )

        assert "--cached" in args

    def test_build_args_with_exclude_standard(self) -> None:
        """Test building args with --exclude-standard flag."""
        args = build_ls_files_args(
            directory=Path("/test"),
            exclude=set(),
            others=False,
            stage=False,
            cached=False,
            exclude_standard=True,
        )

        assert "--exclude-standard" in args

    def test_build_args_with_exclude_patterns(self) -> None:
        """Test building args with exclude patterns."""
        args = build_ls_files_args(
            directory=Path("/test"),
            exclude={"*.pyc", "node_modules"},
            others=False,
            stage=False,
            cached=False,
            exclude_standard=False,
        )

        assert "--exclude=*.pyc" in args or "--exclude=node_modules" in args

    def test_build_args_with_all_options(self) -> None:
        """Test building args with all options enabled."""
        args = build_ls_files_args(
            directory=Path("/test/dir"),
            exclude={"*.log"},
            others=True,
            stage=True,
            cached=True,
            exclude_standard=True,
        )

        assert "--others" in args
        assert "--stage" in args
        assert "--cached" in args
        assert "--exclude-standard" in args
        assert "--exclude=*.log" in args
        assert str(Path("/test/dir")) in args


class TestIndentString:
    """Tests for the indent_string function."""

    def test_zero_indent_returns_empty_string(self) -> None:
        """Test that zero indent count returns empty string."""
        result = indent_string("test", indent_count=0)
        assert result == ""

    def test_indent_with_spaces(self) -> None:
        """Test indentation with spaces."""
        result = indent_string("text", indent_count=2, indent_width=2, indent_type=IndentType.SPACES)
        assert result == "    text"  # 2 * 2 = 4 spaces

    def test_indent_with_tabs(self) -> None:
        """Test indentation with tabs."""
        result = indent_string("text", indent_count=2, indent_width=2, indent_type=IndentType.TABS)
        assert result == "\t\ttext"  # 2 tabs

    def test_indent_with_custom_width(self) -> None:
        """Test indentation with custom width."""
        result = indent_string("x", indent_count=1, indent_width=4, indent_type=IndentType.SPACES)
        assert result == "    x"  # 4 spaces


class TestValidateAndReturnRepo:
    """Tests for the validate_and_return_repo function."""

    def test_valid_repo_returns_repo_object(self, tmp_path) -> None:
        """Test that a valid git repo path returns a Repo object."""
        # Create a git repo
        from git import Repo
        repo_path = tmp_path / "test_repo"
        repo_path.mkdir()
        Repo.init(repo_path)

        result = validate_and_return_repo(repo_path)

        assert result is not None
        assert isinstance(result, Repo)

    def test_invalid_repo_raises_exit(self, tmp_path) -> None:
        """Test that an invalid git repo raises typer.Exit."""
        non_git_path = tmp_path / "not_a_repo"
        non_git_path.mkdir()

        with pytest.raises(typer.Exit) as exc_info:
            validate_and_return_repo(non_git_path)

        assert exc_info.value.exit_code == 1

    def test_nonexistent_path_raises_exit(self) -> None:
        """Test that a non-existent path raises typer.Exit."""
        with pytest.raises(typer.Exit) as exc_info:
            validate_and_return_repo(Path("/nonexistent/path/to/repo"))

        assert exc_info.value.exit_code == 1


class TestValidateAndReturnPath:
    """Tests for the validate_and_return_path function."""

    def test_valid_path_returns_resolved_path(self, tmp_path) -> None:
        """Test that a valid path returns the resolved path."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        result = validate_and_return_path(test_dir)

        assert result == test_dir.resolve()

    def test_nonexistent_path_raises_exit(self) -> None:
        """Test that a non-existent path raises typer.Exit."""
        with pytest.raises(typer.Exit) as exc_info:
            validate_and_return_path(Path("/nonexistent/path"))

        assert exc_info.value.exit_code == 1


class TestEmptyListIfNone:
    """Tests for the empty_list_if_none function."""

    def test_none_returns_empty_list(self) -> None:
        """Test that None returns an empty list."""
        result = empty_list_if_none(None)
        assert result == []

    def test_list_returns_same_list(self) -> None:
        """Test that a list returns the same list."""
        input_list = [1, 2, 3]
        result = empty_list_if_none(input_list)
        assert result == input_list

    def test_empty_list_returns_empty_list(self) -> None:
        """Test that an empty list returns an empty list."""
        result = empty_list_if_none([])
        assert result == []


class TestResolveRepoPaths:
    """Tests for the resolve_repo_paths function."""

    def test_empty_paths_returns_root_node(self) -> None:
        """Test that empty paths returns set containing root node."""
        root = Path("/root")
        result = resolve_repo_paths([], root)
        assert result == {root}

    def test_relative_paths_converted(self, tmp_path) -> None:
        """Test that paths relative to root are correctly resolved."""
        root = tmp_path
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        result = resolve_repo_paths([subdir], root)

        assert Path("subdir") in result

    def test_non_relative_paths_kept_as_is(self, tmp_path) -> None:
        """Test that paths not relative to root are kept as-is."""
        root = tmp_path / "root"
        root.mkdir()
        other_path = tmp_path / "other"
        other_path.mkdir()

        result = resolve_repo_paths([other_path], root)

        # Path that can't be made relative should be kept
        assert other_path in result


class TestValidateDirectories:
    """Tests for the validate_directories function."""

    def test_valid_directories_no_error(self, tmp_path) -> None:
        """Test that valid directories pass validation."""
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        dir2 = tmp_path / "dir2"
        dir2.mkdir()

        # Should not raise
        validate_directories({dir1, dir2})

    def test_file_path_raises_exit(self, tmp_path) -> None:
        """Test that a file path raises typer.Exit."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content")

        with pytest.raises(typer.Exit) as exc_info:
            validate_directories({test_file})

        assert exc_info.value.exit_code == 1


class TestGenerateOutputContent:
    """Tests for the generate_output_content function."""

    def test_yaml_format_returns_yaml(self, mock_path_is_dir) -> None:
        """Test that YAML format generates YAML output."""
        with pytest.MonkeyPatch.context() as mp:
            mock_is_dir = mock_path_is_dir({"root"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            tree = Tree[Path]("Test")
            root = tree.add(Path("root"))
            root.add(Path("file.txt"))

            result = generate_output_content(tree, OutputFormat.YAML, {"--cached"})

            assert "root" in result
            assert "file.txt" in result

    def test_tree_format_returns_tree(self, mock_path_is_dir) -> None:
        """Test that TREE format generates tree output."""
        with pytest.MonkeyPatch.context() as mp:
            mock_is_dir = mock_path_is_dir({"root"})
            mp.setattr(Path, "is_dir", mock_is_dir)

            tree = Tree[Path]("Test")
            root = tree.add(Path("root"))
            root.add(Path("file.txt"))

            result = generate_output_content(tree, OutputFormat.TREE, {"--cached"})

            assert "root" in result
            assert "file.txt" in result

    def test_empty_yaml_returns_message(self) -> None:
        """Test that empty YAML output returns informative message."""
        tree = Tree[Path]("Empty")

        result = generate_output_content(tree, OutputFormat.YAML, {"--others"})

        assert "Nothing found" in result or result == ""


class TestBuildTreeFromGit:
    """Tests for the build_tree_from_git function."""

    def test_build_tree_with_files(self, tmp_path) -> None:
        """Test building a tree from a git repository."""
        from git import Repo

        # Create a git repo with a file
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        test_file = repo_path / "test.txt"
        test_file.write_text("content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        tree = build_tree_from_git(
            repo=repo,
            root_node=repo_path,
            directories={repo_path},
            exclude=set(),
            others=False,
            stage=False,
            cached=True,
            exclude_standard=False,
        )

        assert tree is not None
        # Tree should have content - use format() to get the full tree representation
        tree_output = tree.format()
        assert "test.txt" in tree_output

    def test_build_tree_with_exclude_pattern(self, tmp_path) -> None:
        """Test building a tree with exclusion patterns."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        # Create files
        (repo_path / "keep.txt").write_text("keep")
        (repo_path / "ignore.log").write_text("ignore")
        repo.index.add(["keep.txt", "ignore.log"])
        repo.index.commit("Initial commit")

        tree = build_tree_from_git(
            repo=repo,
            root_node=repo_path,
            directories={repo_path},
            exclude={"*.log"},
            others=False,
            stage=False,
            cached=True,
            exclude_standard=False,
        )

        tree_output = tree.format()
        assert "keep.txt" in tree_output


class TestMainFunction:
    """Tests for the main CLI function."""

    def test_main_with_valid_repo_yaml_output(self, tmp_path) -> None:
        """Test main function with valid repo and YAML output."""
        from git import Repo

        # Create a git repo
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        test_file = repo_path / "test.txt"
        test_file.write_text("content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        output_file = tmp_path / "output.yaml"

        # Change to repo directory and run main
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            main(
                repo_paths=None,
                repo_path=repo_path,
                output=output_file,
                format=OutputFormat.YAML,
                verbose=False,
                exclude=None,
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        assert output_file.exists()
        content = output_file.read_text()
        assert "test.txt" in content

    def test_main_with_tree_format(self, tmp_path) -> None:
        """Test main function with tree format output."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        test_file = repo_path / "test.txt"
        test_file.write_text("content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        output_file = tmp_path / "output.txt"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            main(
                repo_paths=None,
                repo_path=repo_path,
                output=output_file,
                format=OutputFormat.TREE,
                verbose=False,
                exclude=None,
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        assert output_file.exists()

    def test_main_with_verbose_mode(self, tmp_path) -> None:
        """Test main function with verbose mode enabled completes successfully."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        test_file = repo_path / "test.txt"
        test_file.write_text("content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        output_file = tmp_path / "output.yaml"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            # Verbose mode should complete without error
            main(
                repo_paths=None,
                repo_path=repo_path,
                output=output_file,
                format=OutputFormat.YAML,
                verbose=True,
                exclude=None,
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        # Verify output file was created with content
        assert output_file.exists()
        content = output_file.read_text()
        assert "test.txt" in content

    def test_main_with_exclude_patterns(self, tmp_path) -> None:
        """Test main function with exclude patterns."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        (repo_path / "keep.txt").write_text("keep")
        (repo_path / "ignore.log").write_text("ignore")
        repo.index.add(["keep.txt", "ignore.log"])
        repo.index.commit("Initial commit")

        output_file = tmp_path / "output.yaml"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            main(
                repo_paths=None,
                repo_path=repo_path,
                output=output_file,
                format=OutputFormat.YAML,
                verbose=False,
                exclude=["*.log"],
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        content = output_file.read_text()
        assert "keep.txt" in content

    def test_main_with_repo_paths(self, tmp_path) -> None:
        """Test main function with specific repo paths."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        subdir = repo_path / "subdir"
        subdir.mkdir()
        repo = Repo.init(repo_path)

        (subdir / "file.txt").write_text("content")
        repo.index.add(["subdir/file.txt"])
        repo.index.commit("Initial commit")

        output_file = tmp_path / "output.yaml"

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            main(
                repo_paths=[subdir],
                repo_path=repo_path,
                output=output_file,
                format=OutputFormat.YAML,
                verbose=False,
                exclude=None,
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        assert output_file.exists()

    def test_main_without_output_file_completes_successfully(self, tmp_path) -> None:
        """Test main function completes without error when no output file specified."""
        from git import Repo

        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        repo = Repo.init(repo_path)

        test_file = repo_path / "hello.txt"
        test_file.write_text("world")
        repo.index.add(["hello.txt"])
        repo.index.commit("Initial commit")

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_path)
            # Should complete without raising an exception
            main(
                repo_paths=None,
                repo_path=repo_path,
                output=None,
                format=OutputFormat.YAML,
                verbose=False,
                exclude=None,
                others=False,
                stage=False,
                cached=True,
                exclude_standard=False,
                repo_as_root=True,
            )
        finally:
            os.chdir(original_cwd)

        # Function completed successfully without an output file
