#!/usr/bin/env python
import sys
import os
from argparse import ArgumentParser
from os.path import basename

from classes.inference.Sampler import *

def build_parser():
  parser = ArgumentParser()
  parser.add_argument('--png_path', type=str,
                      dest='png_path', help='png filepath to convert into HTML',
                      required=True)
  parser.add_argument('--output_folder', type=str,
                      dest='output_folder', help='dir to save generated gui and html',
                      required=True)
  parser.add_argument('--model_json_file', type=str,
                      dest='model_json_file', help='trained model json file',
                      required=True)
  parser.add_argument('--model_weights_file', type=str,
                      dest='model_weights_file', help='trained model weights file', required=True)
  parser.add_argument('--style', type=str,
                      dest='style', help='style to use for generation', default='default')
  parser.add_argument('--print_generated_output', type=int,
                      dest='print_generated_output', help='see generated GUI output in terminal', default=1)
  parser.add_argument('--print_bleu_score', type=int,
                      dest='print_bleu_score', help='see BLEU score for single example', default=0)
  parser.add_argument('--original_gui_filepath', type=str,
                      dest='original_gui_filepath', help='if getting BLEU score, provide original gui filepath', default=None)

  return parser

def main():
    parser = build_parser()
    options = parser.parse_args()
    png_path = options.png_path
    output_folder = options.output_folder
    model_json_file = options.model_json_file
    model_weights_file = options.model_weights_file
    style = options.style
    print_generated_output = options.print_generated_output
    print_bleu_score = options.print_bleu_score
    original_gui_filepath = options.original_gui_filepath

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sampler = Sampler(model_json_path=model_json_file,
                      model_weights_path = model_weights_file)
    sampler.convert_single_image(output_folder, png_path=png_path, print_generated_output=print_generated_output, get_sentence_bleu=print_bleu_score, original_gui_filepath=original_gui_filepath, style=style)

if __name__ == "__main__":
  main()