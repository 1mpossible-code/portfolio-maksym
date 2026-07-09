#!/bin/bash

cd /root/portfolio-maksym

git fetch && git reset origin/main --hard

source venv/bin/activate
pip install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio

