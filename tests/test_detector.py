"""Tests for the detector module."""

import os
import tempfile
from pathlib import Path

import pytest

from mise_salt_shakers.detector import (
    detect_project_type,
    verify_file_exists,
    get_project_files,
)


class TestDetectProjectType:
    """Tests for the detect_project_type function."""

    def test_detects_python_pyproject(self):
        """Test detection of Python project via pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "pyproject.toml").touch()
            assert detect_project_type(tmpdir) == "python"

    def test_detects_python_requirements(self):
        """Test detection of Python project via requirements.txt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "requirements.txt").touch()
            assert detect_project_type(tmpdir) == "python"

    def test_detects_node_project(self):
        """Test detection of Node.js project via package.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "package.json").touch()
            assert detect_project_type(tmpdir) == "node"

    def test_detects_go_project(self):
        """Test detection of Go project via go.mod."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "go.mod").touch()
            assert detect_project_type(tmpdir) == "go"

    def test_detects_rust_project(self):
        """Test detection of Rust project via Cargo.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Cargo.toml").touch()
            assert detect_project_type(tmpdir) == "rust"

    def test_detects_java_maven(self):
        """Test detection of Java project via pom.xml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "pom.xml").touch()
            assert detect_project_type(tmpdir) == "java"

    def test_detects_java_gradle(self):
        """Test detection of Java project via build.gradle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "build.gradle").touch()
            assert detect_project_type(tmpdir) == "java"

    def test_detects_cpp_project(self):
        """Test detection of C++ project via CMakeLists.txt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "CMakeLists.txt").touch()
            assert detect_project_type(tmpdir) == "c++"

    def test_detects_docker_project(self):
        """Test detection of Docker project via Dockerfile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Dockerfile").touch()
            assert detect_project_type(tmpdir) == "docker"

    def test_detects_docker_compose(self):
        """Test detection of Docker project via docker-compose.yml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "docker-compose.yml").touch()
            assert detect_project_type(tmpdir) == "docker"

    def test_returns_unknown_for_empty_dir(self):
        """Test that unknown is returned when no project files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert detect_project_type(tmpdir) == "unknown"

    def test_defaults_to_current_directory(self):
        """Test that current directory is used when no path is provided."""
        original_cwd = os.getcwd()
        os.chdir("/workspace/project/mise-salt-shakers")
        try:
            result = detect_project_type()
            assert result in ["python", "node", "unknown"]
        finally:
            os.chdir(original_cwd)


class TestVerifyFileExists:
    """Tests for the verify_file_exists function."""

    def test_returns_true_for_existing_file(self):
        """Test that True is returned for an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test.txt").touch()
            assert verify_file_exists("test.txt", tmpdir) is True

    def test_returns_false_for_nonexistent_file(self):
        """Test that False is returned for a nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert verify_file_exists("nonexistent.txt", tmpdir) is False

    def test_returns_false_for_directory(self):
        """Test that False is returned for a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "testdir").mkdir()
            assert verify_file_exists("testdir", tmpdir) is False

    def test_handles_nested_path(self):
        """Test verification of nested file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "subdir").mkdir()
            Path(tmpdir, "subdir", "file.txt").touch()
            assert verify_file_exists("subdir/file.txt", tmpdir) is True

    def test_defaults_to_current_directory(self):
        """Test that current directory is used when no path is provided."""
        original_cwd = os.getcwd()
        os.chdir("/workspace/project/mise-salt-shakers")
        try:
            result = verify_file_exists("pyproject.toml")
            assert result is True
        finally:
            os.chdir(original_cwd)


class TestGetProjectFiles:
    """Tests for the get_project_files function."""

    def test_returns_existing_files(self):
        """Test that only existing files are returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "README.md").touch()
            Path(tmpdir, "pyproject.toml").touch()
            Path(tmpdir, "nonexistent.txt").touch()

            files = get_project_files(tmpdir)
            assert "README.md" in files
            assert "pyproject.toml" in files
            assert "nonexistent.txt" not in files

    def test_returns_empty_list_for_empty_dir(self):
        """Test that empty list is returned for directory with no project files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = get_project_files(tmpdir)
            assert files == []

    def test_includes_license(self):
        """Test that LICENSE file is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "LICENSE").touch()
            files = get_project_files(tmpdir)
            assert "LICENSE" in files

    def test_includes_dockerfile(self):
        """Test that Dockerfile is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Dockerfile").touch()
            files = get_project_files(tmpdir)
            assert "Dockerfile" in files

    def test_defaults_to_current_directory(self):
        """Test that current directory is used when no path is provided."""
        original_cwd = os.getcwd()
        os.chdir("/workspace/project/mise-salt-shakers")
        try:
            result = get_project_files()
            assert isinstance(result, list)
        finally:
            os.chdir(original_cwd)