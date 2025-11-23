#!/usr/bin/env python3
from _library import VersionControl as myVersionControl

commit_message = input("Enter commit message for committing all changes (leave blank for default): ").strip()
myVersionControl.add_and_commit_all(commit_message)

