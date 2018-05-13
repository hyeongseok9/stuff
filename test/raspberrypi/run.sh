#!/bin/bash

cd "$(dirname "$0")"
PYTHONPATH=.:/home/pi/git_repo/:/home/pi/git_repo/lcd python langtest1.py
