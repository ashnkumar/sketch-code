#! /bin/bash
mkdir ../bin
aws s3 cp s3://sketch-code/model_json_weights/model_json.json ../bin/model_json.json
aws s3 cp s3://sketch-code/model_json_weights/weights.h5 ../bin/pretrained_weights.h5
