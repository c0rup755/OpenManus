#!/usr/bin/env python3
"""Run Abuelita Meri bot with option 1 (create one episode)"""

import subprocess
import sys

# Run the bot with input "1" to create one episode
process = subprocess.Popen(
    [sys.executable, "abuelita_meri_bot.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input="1\n")

print(stdout)
if stderr:
    print(stderr, file=sys.stderr)

sys.exit(process.returncode)
