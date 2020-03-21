#!/bin/bash

python3 onlinereso1.py
cp out.txt data.txt
python3 onlinereso1.py
cp out.txt data.txt
python3 onlinereso2.py
cp out.txt data.txt
cat out.txt