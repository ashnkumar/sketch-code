#!/usr/bin/env python
import sys
import os
from argparse import ArgumentParser
from os.path import basename

from classes.inference.Sampler import *

def build_parser():
  parser = ArgumentParser()
  parser.add_argument('--pngs_path', type=str,
                      dest='pngs_path', help='png folder to convert into HTML',
                      required=True)
  parser.add_argument('--output_folder', type=str,
                      dest='output_folder', help='dir to save generated gui and html',
                      required=True)
  parser.add_argument('--model_json_file', type=str,
                      dest='model_json_file', help='trained model json file',
                      required=True)
  parser.add_argument('--model_weights_file', type=str,
                      dest='model_weights_file', help='trained model weights file', required=True)
  parser.add_argument('--print_bleu_score', type=int,
                      dest='print_bleu_score', help='see BLEU score for single example', default=0)
  parser.add_argument('--original_guis_filepath', type=str,
                      dest='original_guis_filepath', help='if getting BLEU score, provide original guis folder filepath', default=None)
  parser.add_argument('--style', type=str,
                      dest='style', help='style to use for generation', default='default')
  return parser

def main():
    parser = build_parser()
    options = parser.parse_args()
    pngs_path = options.pngs_path
    output_folder = options.output_folder
    model_json_file = options.model_json_file
    model_weights_file = options.model_weights_file
    print_bleu_score = options.print_bleu_score
    original_guis_filepath = options.original_guis_filepath
    style = options.style


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create sampler
    sampler = Sampler(model_json_path=model_json_file,
                      model_weights_path = model_weights_file)

    # Sample and retrieve BLEU
    sampler.convert_batch_of_images(output_folder, pngs_path=pngs_path, get_corpus_bleu=print_bleu_score, original_guis_filepath=original_guis_filepath, style=style)

if __name__ == "__main__":
  main()