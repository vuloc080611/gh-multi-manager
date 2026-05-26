import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_git_repo():
    """Tạo một thư mục tạm chứa một git repo giả (có .git)"""
    temp_dir = tempfile.mkdtemp()
    repo_dir = Path(temp_dir) / "fake_repo"
    repo_dir.mkdir()
    (repo_dir / ".git").mkdir()          # chỉ cần thư mục .git là đủ để được coi là git repo
    yield repo_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_github_repo():
    """Mock một đối tượng Repository của PyGithub"""
    from unittest.mock import MagicMock
    mock = MagicMock()
    mock.name = "test-repo"
    mock.clone_url = "https://github.com/user/test-repo.git"
    return mock
