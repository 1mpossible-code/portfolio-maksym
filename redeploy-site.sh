#!/bin/bash

# kill all sessions without an error
tmux kill-server || true

cd /root/portfolio-maksym

git fetch && git reset origin/main --hard

source venv/bin/activate
pip install -r requirements.txt

tmux new-session -d -s "portfolio" -c '/root/portfolio-maksym' 'source venv/bin/activate && flask run --host=0.0.0.0'

