import subprocess
import sys
import time
import argparse
from datetime import datetime, timezone


def in_git_repo():
    return (
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).returncode
        == 0
    )


def get_last_commit_time():
    """Get time since last commit in human readable format"""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return None

    try:
        commit_timestamp = int(result.stdout.strip())
        commit_time = datetime.fromtimestamp(commit_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        diff = now - commit_time

        if diff.days > 0:
            return f"{diff.days}d"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m"
        else:
            return f"{diff.seconds}s"

    except (ValueError, OSError):
        return None


def count_lines():
    # ...  your existing count_lines function ...
    # (keeping the same logic as before)
    diff_result = subprocess.run(
        ["git", "diff", "--unified=0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    tracked_lines = 0
    if diff_result.returncode == 0:
        tracked_lines = sum(
            1
            for line in diff_result.stdout.splitlines()
            if (line.startswith("+") or line.startswith("-"))
            and not line.startswith(("+++", "---"))
        )

    staged_result = subprocess.run(
        ["git", "diff", "--staged", "--unified=0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    staged_lines = 0
    if staged_result.returncode == 0:
        staged_lines = sum(
            1
            for line in staged_result.stdout.splitlines()
            if (line.startswith("+") or line.startswith("-"))
            and not line.startswith(("+++", "---"))
        )

    untracked_result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    untracked_lines = 0
    if untracked_result.returncode == 0:
        for file_path in untracked_result.stdout.splitlines():
            if file_path.strip():
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        untracked_lines += sum(1 for line in f if line.strip())
                except (OSError, IOError):
                    continue

    return tracked_lines + staged_lines + untracked_lines


def emoji(size, time_since=None):
    if size is None:
        return ""

    # Choose emoji based on size
    if size < 20:
        emoji_part = f"🟩 {size}"
    elif size < 100:
        emoji_part = f"🟧 {size}"
    else:
        emoji_part = f"🟥 {size}"

    # Add time since last commit
    if time_since:
        return f"{emoji_part} ⏰{time_since}"
    else:
        return emoji_part


def run_once():
    """Single run mode for prompt integration"""
    if not in_git_repo():
        return

    lines = count_lines()
    time_since = get_last_commit_time()
    print(emoji(lines, time_since), end="")


def run_monitor():
    """Continuous monitoring mode"""
    if not in_git_repo():
        print("Not in a git repository")
        return

    last_status = None

    try:
        while True:
            lines = count_lines()
            time_since = get_last_commit_time()
            current_status = emoji(lines, time_since)

            if current_status != last_status:
                sys.stdout.write("\r\033[K")
                sys.stdout.write(current_status)
                sys.stdout.flush()
                last_status = current_status

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


def run():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Atomic commit change counter")
    parser.add_argument(
        "--monitor", "-m", action="store_true", help="Run in continuous monitoring mode"
    )

    args = parser.parse_args()

    if args.monitor:
        run_monitor()
    else:
        run_once()


if __name__ == "__main__":
    run()
