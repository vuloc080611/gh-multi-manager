import asyncio
import os
from pathlib import Path
from typing import List

from github import Github, GithubException
from github.Repository import Repository

from gh_multi.utils import run_git_command


def get_github_user_repos(username: str) -> List[Repository]:
    """Lấy danh sách repository public của user (hoặc private nếu có token)."""
    token = os.environ.get("GITHUB_TOKEN")
    g = Github(token) if token else Github()
    try:
        user = g.get_user(username)
        repos = user.get_repos()
        return list(repos)
    except GithubException as e:
        print(f"GitHub API error: {e}")
        return []


def clone_all_repos(repos: List[Repository], output_dir: Path):
    """Clone đồng bộ (có thể nâng cấp lên asyncio sau)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for repo in repos:
        clone_url = repo.clone_url
        repo_name = repo.name
        target = output_dir / repo_name
        if target.exists():
            print(f"⏭️  Skipping {repo_name} (already exists)")
            continue
        cmd = ["git", "clone", clone_url, str(target)]
        run_git_command(cmd)
        print(f"✅ Cloned {repo_name}")
