#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

from argparse import ArgumentParser

from classes.model.SketchCodeModel import *

VAL_SPLIT = 0.2

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--data_input_path', type=str,
                        dest='data_input_path', help='directory containing images and guis',
                        required=True)
    parser.add_argument('--validation_split', type=float,
                        dest='validation_split', help='portion of training data for validation set',
                        default=VAL_SPLIT)
    parser.add_argument('--epochs', type=int,
                        dest='epochs', help='number of epochs to train on',
                        required=True)
    parser.add_argument('--model_output_path', type=str,
                        dest='model_output_path', help='directory for saving model data',
                        required=True)
    parser.add_argument('--model_json_file', type=str,
                        dest='model_json_file', help='pretrained model json file',
                        required=False)
    parser.add_argument('--model_weights_file', type=str,
                        dest='model_weights_file', help='pretrained model weights file',
                        required=False)
    parser.add_argument('--augment_training_data', type=int,
                        dest='augment_training_data', help='use Keras image augmentation on training data',
                        default=1)
    return parser

def main():

    parser = build_parser()
    options = parser.parse_args()
    data_input_path = options.data_input_path
    validation_split = options.validation_split
    epochs = options.epochs
    model_output_path = options.model_output_path
    model_json_file = options.model_json_file
    model_weights_file = options.model_weights_file
    augment_training_data = options.augment_training_data

    # Load model
    model = SketchCodeModel(model_output_path, model_json_file, model_weights_file)

    # Create the model output path if it doesn't exist
    if not os.path.exists(model_output_path):
        os.makedirs(model_output_path)

    # Split the datasets and save down image arrays
    training_path, validation_path = ModelUtils.prepare_data_for_training(data_input_path, validation_split, augment_training_data)

    # Begin model training
    model.train(training_path=training_path,
                validation_path=validation_path,
                epochs=epochs)

if __name__ == "__main__":
    main()