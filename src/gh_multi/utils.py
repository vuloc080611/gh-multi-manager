import subprocess
from pathlib import Path
from typing import List, Dict, Any


def run_git_command(cmd: List[str], cwd: Path = None) -> Dict[str, Any]:
    """Run git command, return {success, stdout, stderr}."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=False
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}


def get_all_repo_paths(base_dir: Path) -> List[Path]:
    """Tìm tất cả thư mục con chứa .git (chỉ cấp 1)."""
    repos = []
    for item in base_dir.iterdir():
        if item.is_dir() and (item / ".git").exists():
            repos.append(item)
    return repos


def get_repo_status(repo_path: Path) -> Dict:
    """Trả về branch hiện tại, có dirty không, ahead/behind so với remote."""
    # Lấy branch hiện tại
    branch_result = run_git_command(["git", "branch", "--show-current"], cwd=repo_path)
    branch = branch_result["stdout"] if branch_result["success"] else "unknown"

    # Kiểm tra dirty (có file thay đổi chưa commit)
    status_result = run_git_command(["git", "status", "--porcelain"], cwd=repo_path)
    is_dirty = bool(status_result["stdout"])

    # Lấy ahead/behind (cần fetch trước? nhẹ thì không fetch, dùng remote)
    # Đơn giản: git rev-list --count origin/<branch>..<branch>
    ahead = 0
    behind = 0
    if branch != "unknown":
        remote_branch = f"origin/{branch}"
        ahead_res = run_git_command(
            ["git", "rev-list", "--count", f"{remote_branch}..{branch}"], cwd=repo_path
        )
        behind_res = run_git_command(
            ["git", "rev-list", "--count", f"{branch}..{remote_branch}"], cwd=repo_path
        )
        if ahead_res["success"]:
            ahead = int(ahead_res["stdout"] or 0)
        if behind_res["success"]:
            behind = int(behind_res["stdout"] or 0)

    return {"branch": branch, "is_dirty": is_dirty, "ahead": ahead, "behind": behind}


def pull_all_repos(repos: List[Path]) -> List[Dict]:
    results = []
    for r in repos:
        res = run_git_command(["git", "pull"], cwd=r)
        results.append({"path": str(r), "success": res["success"], "output": res["stdout"]})
    return results


def commit_and_push_all(repos: List[Path], commit_msg: str):
    # Triển khai tương tự – bạn có thể tự thêm hoặc mình viết tiếp nếu cần
    pass


def create_branch_all(repos: List[Path], branch_name: str):
    pass
