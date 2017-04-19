#!/bin/bash
rm -rf trick
mkdir trick

cp ./client.py ./trick
cd trick
pyinstaller --onefile client.py
