#!/usr/bin/bash

set -x

# Copy files to the server
source "scripts/.env"
rsync -azrvh --progress -e "ssh -p $PORT" --exclude={'*.db','.venv','.git','node_modules','.ruff*','__pycache__'} "$SOURCE" $HOST:$DEST

# Reload application
ssh $HOST -p $PORT -t "cd $DEST && make build && make restart"
