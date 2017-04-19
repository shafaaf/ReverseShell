#!/bin/bash

# This makes the standalone executable under trick folder

rm -rf trick
mkdir trick

cp ./client.py ./trick
cd trick
pyinstaller --onefile client.py

cd dist
