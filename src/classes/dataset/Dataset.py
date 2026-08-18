from __future__ import absolute_import

import os
import shutil
import pdb
import hashlib
import numpy as np

from tensorflow.keras.preprocessing.text import Tokenizer, one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from .ImagePreprocessor import *

VOCAB_FILE              = '../vocabulary.vocab'
TRAINING_SET_NAME       = "training_set"
VALIDATION_SET_NAME     = "validation_set"
BATCH_SIZE              = 64

class Dataset:

    def __init__(self, data_input_folder, test_set_folder=None):
        self.data_input_folder = data_input_folder
        self.test_set_folder   = test_set_folder

    def split_datasets(self, validation_split):
        sample_ids = self.populate_sample_ids()
        print("Total number of samples: ", len(sample_ids))

        train_set_ids, val_set_ids, shuffled_sampled_ids = self.get_all_id_sets(validation_split, sample_ids)
        training_path, validation_path = self.split_samples(train_set_ids, val_set_ids)

        return training_path, validation_path

    def split_samples(self, train_set_ids, val_set_ids):
        training_path, validation_path = self.create_data_folders()
        self.copy_files_to_folders(train_set_ids, training_path)
        self.copy_files_to_folders(val_set_ids, validation_path)
        return training_path, validation_path

    def preprocess_data(self, training_path, validation_path, augment_training_data):
        train_img_preprocessor = ImagePreprocessor()
        train_img_preprocessor.build_image_dataset(training_path, augment_data=augment_training_data)
        val_img_preprocessor = ImagePreprocessor()
        val_img_preprocessor.build_image_dataset(validation_path, augment_data=0)




    ##########################################
    ####### PRIVATE METHODS ##################
    ##########################################

    @classmethod
    def load_vocab(cls):
        file = open(VOCAB_FILE, 'r')
        text = file.read().splitlines()[0]
        file.close()
        tokenizer = Tokenizer(filters='', split=" ", lower=False)
        tokenizer.fit_on_texts([text])
        vocab_size = len(tokenizer.word_index) + 1
        return tokenizer, vocab_size

    @classmethod
    def create_generator(cls, data_input_path, max_sequences):
        img_features, text_features = Dataset.load_data(data_input_path)
        total_sequences = 0
        for text_set in text_features: total_sequences += len(text_set.split())
        steps_per_epoch = total_sequences // BATCH_SIZE
        tokenizer, vocab_size = Dataset.load_vocab()
        data_gen = Dataset.data_generator(text_features, img_features, max_sequences, tokenizer, vocab_size)
        return data_gen, steps_per_epoch

    @classmethod
    def data_generator(cls, text_features, img_features, max_sequences, tokenizer, vocab_size):
        while 1:
            for i in range(0, len(text_features), 1):
                Ximages, XSeq, y = list(), list(),list()
                for j in range(i, min(len(text_features), i+1)):
                    image = img_features[j]
                    desc = text_features[j]
                    in_img, in_seq, out_word = Dataset.process_data_for_generator([desc], [image], max_sequences, tokenizer, vocab_size)
                    for k in range(len(in_img)):
                        Ximages.append(in_img[k])
                        XSeq.append(in_seq[k])
                        y.append(out_word[k])
                yield [[np.array(Ximages), np.array(XSeq)], np.array(y)]

    @classmethod
    def process_data_for_generator(cls, texts, features, max_sequences, tokenizer, vocab_size):
        X, y, image_data = list(), list(), list()
        sequences = tokenizer.texts_to_sequences(texts)
        for img_no, seq in enumerate(sequences):
            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]
                in_seq = pad_sequences([in_seq], maxlen=max_sequences)[0]
                out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                image_data.append(features[img_no])
                X.append(in_seq[-48:])
                y.append(out_seq)
        return np.array(image_data), np.array(X), np.array(y)

    @classmethod
    def load_data(cls, data_input_path):
        text = []
        images = []
        all_filenames = os.listdir(data_input_path)
        all_filenames.sort()
        for filename in all_filenames:
            if filename[-3:] == "npz":
                image = np.load(data_input_path+'/'+filename)
                images.append(image['features'])
            elif filename[-3:] == 'gui':
                file = open(data_input_path+'/'+filename, 'r')
                texts = file.read()
                file.close()
                syntax = '<START> ' + texts + ' <END>'
                syntax = ' '.join(syntax.split())
                syntax = syntax.replace(',', ' ,')
                text.append(syntax)
        images = np.array(images, dtype=float)
        return images, text

    def create_data_folders(self):
        training_path = "{}/{}".format(os.path.dirname(self.data_input_folder), TRAINING_SET_NAME)
        validation_path = "{}/{}".format(os.path.dirname(self.data_input_folder), VALIDATION_SET_NAME)

        self.delete_existing_folders(training_path)
        self.delete_existing_folders(validation_path)

        if not os.path.exists(training_path): os.makedirs(training_path)
        if not os.path.exists(validation_path): os.makedirs(validation_path)
        return training_path, validation_path

    def copy_files_to_folders(self, sample_ids, output_folder):
        copied_count = 0
        for sample_id in sample_ids:
            sample_id_png_path = "{}/{}.png".format(self.data_input_folder, sample_id)
            sample_id_gui_path = "{}/{}.gui".format(self.data_input_folder, sample_id)
            if os.path.exists(sample_id_png_path) and os.path.exists(sample_id_gui_path):
                output_png_path = "{}/{}.png".format(output_folder, sample_id)
                output_gui_path = "{}/{}.gui".format(output_folder, sample_id)
                shutil.copyfile(sample_id_png_path, output_png_path)
                shutil.copyfile(sample_id_gui_path, output_gui_path)
                copied_count += 1
        print("Moved {} files from {} to {}".format(copied_count, self.data_input_folder, output_folder))

    def delete_existing_folders(self, folder_to_delete):
        if os.path.exists(folder_to_delete):
            shutil.rmtree(folder_to_delete)
            print("Deleted existing folder: {}".format(folder_to_delete))

    def populate_sample_ids(self):
        all_sample_ids = []
        full_path = os.path.realpath(self.data_input_folder)
        for f in os.listdir(full_path):
            if f.find(".gui") != -1:
                file_name = f[:f.find(".gui")]
                if os.path.isfile("{}/{}.png".format(self.data_input_folder, file_name)):
                    all_sample_ids.append(file_name)
        return all_sample_ids

    def get_all_id_sets(self, validation_split, sample_ids):
        np.random.shuffle(sample_ids)
        val_count = int(validation_split * len(sample_ids))
        train_count = len(sample_ids) - val_count
        print("Splitting datasets, training samples: {}, validation samples: {}".format(train_count, val_count))
        train_set, val_set = self.split_paths(sample_ids, train_count, val_count)

        return train_set, val_set, sample_ids

    def split_paths(self, sample_ids, train_count, val_count):
        train_set = []
        val_set = []
        hashes = []
        for sample_id in sample_ids:
            f = open("{}/{}.gui".format(self.data_input_folder, sample_id), 'r', encoding='utf-8')

            with f:
                chars = ""
                for line in f:
                    chars += line
                content_hash = chars.replace(" ", "").replace("\n", "")
                content_hash = hashlib.sha256(content_hash.encode('utf-8')).hexdigest()

                if len(val_set) == val_count:
                    train_set.append(sample_id)
                else:
                    is_unique = True
                    for h in hashes:
                        if h is content_hash:
                            is_unique = False
                            break

                    if is_unique:
                        val_set.append(sample_id)
                    else:
                        train_set.append(sample_id)

                hashes.append(content_hash)

        assert len(val_set) == val_count

        return train_set, val_set
