#!/bin/bash
hashdeep ../testfolder/test.java > ../testhashes/tempFile.txt
python getFileHash.py 
