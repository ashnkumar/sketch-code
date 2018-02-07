#! /bin/bash
mkdir ../data
aws s3 cp s3://sketch-code/data/all_data.zip ../data/all_data.zip
unzip ../data/all_data.zip -d ../data/all_data
