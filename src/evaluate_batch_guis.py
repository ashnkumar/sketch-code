#!/usr/bin/env python
from __future__ import print_function

from argparse import ArgumentParser

from classes.inference.Evaluator import *

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--original_guis_filepath', type=str,
                        dest='original_guis_filepath', help='dir with all original guis',
                        required=True)
    parser.add_argument('--predicted_guis_filepath', type=str,
                        dest='predicted_guis_filepath', help='dir with all predicted guis',
                        required=True)
    return parser

def main():

    parser = build_parser()
    options = parser.parse_args()
    original_guis_filepath = options.original_guis_filepath
    predicted_guis_filepath = options.predicted_guis_filepath

    bleu_score = Evaluator.get_corpus_bleu(original_guis_filepath, predicted_guis_filepath)
    print("BLEU score for batch of GUIs: {}".format(bleu_score))

if __name__ == "__main__":
    main()