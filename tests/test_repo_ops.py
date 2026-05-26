import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
from gh_multi.repo_ops import get_github_user_repos, clone_all_repos


@patch("gh_multi.repo_ops.Github")
def test_get_github_user_repos_public_no_token(mock_github_class):
    """Test lấy danh sách repo public khi không có GITHUB_TOKEN"""
    # Tạo mock user và repos
    mock_user = MagicMock()
    mock_repo1 = MagicMock()
    mock_repo1.name = "repo1"
    mock_repo2 = MagicMock()
    mock_repo2.name = "repo2"
    mock_user.get_repos.return_value = [mock_repo1, mock_repo2]

    mock_github_instance = MagicMock()
    mock_github_instance.get_user.return_value = mock_user
    mock_github_class.return_value = mock_github_instance

    repos = get_github_user_repos("testuser")

    assert len(repos) == 2
    assert repos[0].name == "repo1"
    mock_github_class.assert_called_once_with()  # không có token


@patch("gh_multi.repo_ops.Github")
def test_get_github_user_repos_with_token(mock_github_class):
    """Test có GITHUB_TOKEN -> nên gọi Github với token"""
    import os
    os.environ["GITHUB_TOKEN"] = "fake-token"
    mock_github_class.return_value.get_user.return_value.get_repos.return_value = []

    repos = get_github_user_repos("anyuser")

    mock_github_class.assert_called_once_with("fake-token")
    # clean up
    del os.environ["GITHUB_TOKEN"]


@patch("gh_multi.repo_ops.run_git_command")
def test_clone_all_repos_skip_existing(mock_run_git, tmp_path, mock_github_repo):
    """Clone bỏ qua repo đã tồn tại"""
    output_dir = tmp_path / "cloned"
    output_dir.mkdir()
    # Tạo thư mục giả cho repo đã tồn tại
    existing = output_dir / "test-repo"
    existing.mkdir()

    repos = [mock_github_repo]
    clone_all_repos(repos, output_dir)

    # run_git_command chỉ được gọi nếu repo chưa tồn tại -> ở đây không gọi
    mock_run_git.assert_not_called()


@patch("gh_multi.repo_ops.run_git_command")
def test_clone_all_repos_clones_new(mock_run_git, tmp_path, mock_github_repo):
    """Clone repo mới khi chưa tồn tại"""
    output_dir = tmp_path / "cloned"
    repos = [mock_github_repo]

    clone_all_repos(repos, output_dir)

    expected_cmd = ["git", "clone", "https://github.com/user/test-repo.git", str(output_dir / "test-repo")]
    mock_run_git.assert_called_once_with(expected_cmd)
