#!/usr/bin/bash

set -x

# Copy files to the server
source ".env"
rsync -azrvh --progress -e "ssh -p $PORT" --exclude={'.venv','.git','node_modules','.ruff*','__pycache__'} "$SOURCE" $HOST:$DEST

# Reload nginx
ssh $HOST -p $PORT -t nginx -s reload
