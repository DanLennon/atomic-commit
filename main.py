import os
import subprocess
import time

RESET = "\033[0m"

def count_lines():
    result = subprocess.run(
        ["git", "diff", "--unified=0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return 0  # Not a git repo or no changes

    count = sum(
        1
        for line in result.stdout.splitlines()
        if (line.startswith("+") or line.startswith("-"))
        and not line.startswith(("+++", "---", "@@"))
    )
    return count

def set_colour(size):
    if size < 20:
        return "\033[42m"  # Green
    elif size < 100:
        return "\033[43m"  # Yellow/Orange
    else:
        return "\033[41m"  # Red

def print_score(colour, total):
    print(colour + f"   Lines {total:4} LOC   " + RESET)

prev = None
while True:
    total = count_lines()
    if total != prev:
        os.system("clear")
        color = set_colour(total)
        print_score(color, total)
        prev = total
    time.sleep(0.5)

