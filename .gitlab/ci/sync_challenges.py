import os
import sys
import traceback
from pathlib import Path
from ctfcli.cli.challenges import ChallengeCommand


cli = ChallengeCommand()

CATEGORIES = map(Path, Path(".categories").read_text().splitlines())

# Get each challenge.yml
chall_list = []
for category in CATEGORIES:
    for root, dirs, files in category.walk():
        for file in files:
            if file == "challenge.yml":
                try:
                    code = cli.install(root.as_posix(), True)
                    assert code == 0
                except Exception as e:
                    print(f"[!!!] Error with challenge {root.as_posix()}")
                    print(e)
                    print(traceback.format_exc())
                    print(sys.exc_info()[2])

