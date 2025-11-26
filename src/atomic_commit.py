import subprocess
import time
import sys


def in_git_repo():
    return (
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).returncode
        == 0
    )


def count_lines():
    # Count lines in tracked file changes
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

    # Count lines in staged changes
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

    # Count lines in untracked files
    untracked_result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    untracked_lines = 0
    if untracked_result.returncode == 0:
        for file_path in untracked_result.stdout.splitlines():
            if file_path.strip():  # Skip empty lines
                try:
                    # Count lines in each untracked file
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        untracked_lines += sum(1 for line in f if line.strip())
                except (OSError, IOError):
                    # Skip files that can't be read (binary, permissions, etc.)
                    continue

    return tracked_lines + staged_lines + untracked_lines


def emoji(size):
    if size is None:
        return ""
    if size < 20:
        return f"🟩 {size}"
    elif size < 100:
        return f"🟧 {size}"
    return f"🟥 {size}"


def run():
    if not in_git_repo():
        print("Not in a git repository")
        return

    last_status = None

    try:
        while True:
            lines = count_lines()
            current_status = emoji(lines)

            # Only update display if status changed
            if current_status != last_status:
                print(f"\r{current_status}", end="", flush=True)
                last_status = current_status

            time.sleep(0.5)  # Check every half second
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    run()
