import pytest
from click.testing import CliRunner
from gh_multi.cli import cli
from unittest.mock import patch, MagicMock


def test_clone_command_success():
    """Test lệnh clone gọi đúng hàm và in ra thông báo"""
    runner = CliRunner()
    with patch("gh_multi.cli.get_github_user_repos") as mock_get_repos, \
         patch("gh_multi.cli.clone_all_repos") as mock_clone:

        mock_repo = MagicMock()
        mock_get_repos.return_value = [mock_repo, mock_repo]  # 2 repos

        result = runner.invoke(cli, ["clone", "--user", "testuser", "--output", "/fake/path"])

        assert result.exit_code == 0
        assert "Found 2 repositories" in result.output
        mock_get_repos.assert_called_once_with("testuser")
        mock_clone.assert_called_once()


def test_clone_command_no_repos():
    """Khi không có repo nào -> thông báo lỗi"""
    runner = CliRunner()
    with patch("gh_multi.cli.get_github_user_repos", return_value=[]):
        result = runner.invoke(cli, ["clone", "--user", "emptyuser"])
        assert "No public repos found" in result.output


def test_pull_command_no_repos(tmp_path):
    """Chạy lệnh pull trong thư mục không có repo nào"""
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["pull"])
        assert "No Git repositories found" in result.output


@patch("gh_multi.cli.get_all_repo_paths")
@patch("gh_multi.cli.pull_all_repos")
def test_pull_command_success(mock_pull_all, mock_get_paths, tmp_path):
    mock_get_paths.return_value = [tmp_path / "repo1", tmp_path / "repo2"]
    mock_pull_all.return_value = [{"success": True}, {"success": True}]

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Tạo thư mục giả để get_all_repo_paths trả về
        (tmp_path / "repo1").mkdir()
        (tmp_path / "repo2").mkdir()
        result = runner.invoke(cli, ["pull"])

    assert result.exit_code == 0
    assert "Pulled 2/2 repos" in result.output
    mock_pull_all.assert_called_once()


@patch("gh_multi.cli.get_all_repo_paths")
@patch("gh_multi.cli.get_repo_status")
def test_status_command_output(mock_get_status, mock_get_paths, tmp_path):
    """Kiểm tra lệnh status hiển thị bảng đẹp"""
    fake_repo = tmp_path / "myrepo"
    fake_repo.mkdir()
    mock_get_paths.return_value = [fake_repo]
    mock_get_status.return_value = {
        "branch": "main",
        "is_dirty": True,
        "ahead": 1,
        "behind": 0
    }

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    # Kiểm tra các từ khoá xuất hiện trong output
    assert "myrepo" in result.output
    assert "main" in result.output
    assert "Yes" in result.output   # Dirty? = Yes
    assert "🔼 1 / 🔽 0" in result.output
