from __future__ import absolute_import

from classes.dataset.Dataset import *

class ModelUtils:

    @staticmethod
    def prepare_data_for_training(data_input_folder, validation_split, augment_training_data):

        dataset = Dataset(data_input_folder)
        training_path, validation_path = dataset.split_datasets(validation_split)
        dataset.preprocess_data(training_path, validation_path, augment_training_data)

        return training_path, validation_path