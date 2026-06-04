"""Utility functions for project detection and verification."""

import os
from pathlib import Path
from typing import Optional


def detect_project_type(repo_path: Optional[str] = None) -> str:
    """
    Detect the project type based on common files.

    Args:
        repo_path: Path to the repository. Defaults to current directory.

    Returns:
        The detected project type as a lowercase string.
        Returns "unknown" if no project type is detected.
    """
    if repo_path is None:
        repo_path = "."

    path = Path(repo_path)

    project_indicators = {
        "node": ["package.json"],
        "python": ["pyproject.toml", "requirements.txt", "setup.py"],
        "go": ["go.mod"],
        "rust": ["Cargo.toml"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        ".net": [".sln", ".csproj"],
        "c++": ["CMakeLists.txt"],
        "docker": ["Dockerfile", "docker-compose.yml", "compose.yml"],
    }

    for project_type, files in project_indicators.items():
        for filename in files:
            if (path / filename).exists():
                return project_type

    return "unknown"


def verify_file_exists(filepath: str, repo_path: Optional[str] = None) -> bool:
    """
    Verify that a file exists in the repository.

    Args:
        filepath: Path to the file relative to repo_path.
        repo_path: Path to the repository. Defaults to current directory.

    Returns:
        True if the file exists, False otherwise.
    """
    if repo_path is None:
        repo_path = "."

    full_path = Path(repo_path) / filepath
    return full_path.exists() and full_path.is_file()


def get_project_files(repo_path: Optional[str] = None) -> list[str]:
    """
    Get a list of common project files in the repository.

    Args:
        repo_path: Path to the repository. Defaults to current directory.

    Returns:
        List of file paths that exist in the repository.
    """
    if repo_path is None:
        repo_path = "."

    path = Path(repo_path)

    common_files = [
        "README.md",
        "LICENSE",
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "Dockerfile",
    ]

    existing_files = []
    for filename in common_files:
        if (path / filename).exists():
            existing_files.append(filename)

    return existing_files