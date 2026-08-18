from __future__ import absolute_import

import sys
import os
import shutil
import json
import numpy as np

from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

from classes.dataset.Dataset import *
from classes.dataset.ImagePreprocessor import *
from .Evaluator import *
from .Compiler import *

MAX_LENGTH = 48

class Sampler:

    def __init__(self, model_json_path=None, model_weights_path=None):
        self.tokenizer, self.vocab_size = Dataset.load_vocab()
        self.model = self.load_model(model_json_path, model_weights_path)

    def convert_batch_of_images(self, output_folder, pngs_path, get_corpus_bleu, original_guis_filepath, style):

        all_filenames = os.listdir(pngs_path)
        all_filenames.sort()
        generated_count = 0
        for filename in all_filenames:
            if filename.find('.png') != -1:
                png_path = "{}/{}".format(pngs_path, filename)
                try:
                    self.convert_single_image(output_folder, png_path, print_generated_output=0, get_sentence_bleu=0, original_gui_filepath=png_path, style=style)
                    generated_count += 1
                except:
                    print("Error with GUI / HTML generation:", sys.exc_info()[0])
                    print(sys.exc_info())
                    continue
        print("Generated code for {} images".format(generated_count))

        if (get_corpus_bleu == 1) and (original_guis_filepath is not None):
            print("BLEU score: {}".format(Evaluator.get_corpus_bleu(original_guis_filepath, output_folder)))

    def convert_single_image(self, output_folder, png_path, print_generated_output, get_sentence_bleu, original_gui_filepath, style):

        # Retrieve sample ID
        png_filename = os.path.basename(png_path)
        if png_filename.find('.png') == -1:
            raise ValueError("Image is not a png!")
        sample_id = png_filename[:png_filename.find('.png')]

        # Generate GUI
        print("Generating code for sample ID {}".format(sample_id))
        generated_gui, gui_output_filepath= self.generate_gui(png_path, print_generated_output=print_generated_output, output_folder=output_folder, sample_id=sample_id)

        # Generate HTML
        generated_html = self.generate_html(generated_gui, sample_id, print_generated_output=print_generated_output, output_folder=output_folder, style=style)

        # Get BLEU
        if get_sentence_bleu == 1 and (original_gui_filepath is not None):
            print("BLEU score: {}".format(Evaluator.get_sentence_bleu(original_gui_filepath, gui_output_filepath)))


    ##########################################
    ####### PRIVATE METHODS ##################
    ##########################################

    def load_model(self, model_json_path, model_weights_path):
        json_file = open(model_json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(model_weights_path)
        print("\nLoaded model from disk")
        return loaded_model

    def generate_gui(self, png_path, print_generated_output, sample_id, output_folder):
        test_img_preprocessor = ImagePreprocessor()
        img_features = test_img_preprocessor.get_img_features(png_path)

        in_text = '<START> '
        photo = np.array([img_features])
        for i in range(150):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
            yhat = self.model.predict([photo, sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = self.word_for_id(yhat)
            if word is None:
                break
            in_text += word + ' '
            if word == '<END>':
                break

        generated_gui = in_text.split()

        if print_generated_output is 1:
            print("\n=========\nGenerated GUI code:")
            print(generated_gui)

        gui_output_filepath = self.write_gui_to_disk(generated_gui, sample_id, output_folder)

        return generated_gui, gui_output_filepath

    def generate_html(self, gui_array, sample_id, print_generated_output, output_folder, style='default'):

        compiler = Compiler(style)
        compiled_website = compiler.compile(gui_array)

        if print_generated_output is 1:
            print("\nCompiled HTML:")
            print(compiled_website)

        if compiled_website != 'HTML Parsing Error':
            output_filepath = "{}/{}.html".format(output_folder, sample_id)
            with open(output_filepath, 'w') as output_file:
                output_file.write(compiled_website)
                print("Saved generated HTML to {}".format(output_filepath))

    def word_for_id(self, integer):
        for word, index in self.tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def write_gui_to_disk(self, gui_array, sample_id, output_folder):
        gui_output_filepath = "{}/{}.gui".format(output_folder, sample_id)
        with open(gui_output_filepath, 'w') as out_f:
            out_f.write(' '.join(gui_array))
        return gui_output_filepath






