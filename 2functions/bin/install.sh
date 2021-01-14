#!/bin/bash
sudo yum install -y git

git config --global user.name "Michael Shaw"
git config --global user.email "micptolshaw@gmail.com"

git config --global color.ui true
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

git clone https://github.com/MYOB-Technology/pgol-backup-rds.git

