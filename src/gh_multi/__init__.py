import asyncio
import os
from pathlib import Path

import click
from tabulate import tabulate

from gh_multi.repo_ops import clone_all_repos, get_github_user_repos
from gh_multi.utils import (
    get_all_repo_paths,
    get_repo_status,
    pull_all_repos,
    commit_and_push_all,
    create_branch_all,
)


@click.group()
def cli():
    """Gh-multi — quản lý hàng loạt GitHub repo từ command line."""
    if "GITHUB_TOKEN" not in os.environ:
        click.secho(
            "⚠️  Warning: GITHUB_TOKEN environment variable not set. "
            "Some operations may fail.",
            fg="yellow",
        )


@cli.command()
@click.option("--user", required=True, help="GitHub username")
@click.option("--output", default="./repos", help="Thư mục để clone repo vào")
def clone(user, output):
    """Clone tất cả repository của một user GitHub."""
    click.echo(f"🔍 Fetching repos for {user}...")
    repos = get_github_user_repos(user)
    if not repos:
        click.echo("❌ No public repos found.")
        return
    click.echo(f"📦 Found {len(repos)} repositories. Starting clone...")
    clone_all_repos(repos, Path(output))
    click.secho("✅ Done!", fg="green")


@cli.command()
def pull():
    """Pull latest changes in all repos inside current directory."""
    repos = get_all_repo_paths(Path.cwd())
    if not repos:
        click.echo("❌ No Git repositories found in current directory.")
        return
    click.echo(f"🔄 Pulling {len(repos)} repositories...")
    results = pull_all_repos(repos)
    success = sum(1 for r in results if r["success"])
    click.secho(f"✅ Pulled {success}/{len(repos)} repos.", fg="green")


@cli.command()
def status():
    """Show status (dirty, ahead/behind) for all repos in current directory."""
    repos = get_all_repo_paths(Path.cwd())
    if not repos:
        click.echo("❌ No Git repositories found.")
        return
    table = []
    for path in repos:
        name = path.name
        stats = get_repo_status(path)
        table.append(
            [
                name,
                stats["branch"],
                "✅ Yes" if stats["is_dirty"] else "❌ No",
                f"🔼 {stats['ahead']} / 🔽 {stats['behind']}"
                if stats["ahead"] or stats["behind"]
                else "✅ up-to-date",
            ]
        )
    click.echo(tabulate(table, headers=["Repository", "Branch", "Dirty?", "Ahead/Behind"], tablefmt="github"))
