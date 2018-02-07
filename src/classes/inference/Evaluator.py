from __future__ import print_function
from __future__ import absolute_import

import pdb
import os
import operator
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

class Evaluator:
    def __init__(self):
        pass

    @classmethod
    def get_sentence_bleu(cls, original_gui_filepath, generated_gui_filepath):
        original_gui = Evaluator.load_gui_doc(original_gui_filepath)
        generated_gui = Evaluator.load_gui_doc(generated_gui_filepath)
        hypothesis = generated_gui[1:-1]
        reference = original_gui
        references = [reference]
        return sentence_bleu(references, hypothesis)

    @classmethod
    def get_corpus_bleu(cls, original_guis_filepath, predicted_guis_filepath):
        actuals, predicted = Evaluator.load_guis_from_folder(original_guis_filepath, predicted_guis_filepath)
        regular_bleu = corpus_bleu(actuals, predicted)
        return regular_bleu

    @classmethod
    def load_gui_doc(cls, gui_filepath):
        file = open(gui_filepath, 'r')
        gui = file.read()
        file.close()
        gui = ' '.join(gui.split())
        gui = gui.replace(',', ' ,')
        gui = gui.split()

        # Predicted images don't have color so we normalize all buttons to btn-orange or btn-active
        btns_to_replace = ['btn-green', 'btn-red']
        normalized_gui = ['btn-orange' if token in btns_to_replace else token for token in gui]
        normalized_gui = ['btn-active' if token == 'btn-inactive' else token for token in normalized_gui]
        return normalized_gui

    @classmethod
    def load_guis_from_folder(cls, original_guis_filepath, predicted_guis_filepath):
        actuals, predicted = list(), list()
        all_files = os.listdir(predicted_guis_filepath)
        all_predicted_files = os.listdir(predicted_guis_filepath)
        all_predicted_guis = [f for f in all_predicted_files if f.find('.gui') != -1]
        all_predicted_guis.sort()
        guis = []
        for f in all_predicted_guis:
            generated_gui_filepath = "{}/{}".format(predicted_guis_filepath, f)
            actual_gui_filepath = "{}/{}".format(original_guis_filepath, f)
            if os.path.isfile(actual_gui_filepath):
                predicted_gui = Evaluator.load_gui_doc(generated_gui_filepath)
                actual_gui = Evaluator.load_gui_doc(actual_gui_filepath)

                predicted.append(predicted_gui[1:-1])
                actuals.append([actual_gui])
        return actuals, predicted