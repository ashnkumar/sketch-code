# SketchCode

![](https://img.shields.io/badge/python-3-brightgreen.svg) ![](https://img.shields.io/badge/tensorflow-1.1.0-orange.svg)

*Generating HTML Code from a hand-drawn wireframe*

![Preview](https://github.com/ashnkumar/sketch-code/blob/master/header_image.png)

SketchCode is a deep learning model that takes hand-drawn web mockups and converts them into working HTML code. It uses an [image captioning](https://towardsdatascience.com/image-captioning-in-deep-learning-9cd23fb4d8d2) architecture to generate its HTML markup from hand-drawn website wireframes.

For more information, check out this post: [Automating front-end development with deep learning](https://blog.insightdatascience.com/automated-front-end-development-using-deep-learning-3169dd086e82)

This project builds on the synthetically generated dataset and model architecture from [pix2code](https://github.com/tonybeltramelli/pix2code) by [Tony Beltramelli](https://github.com/tonybeltramelli) and the [Design Mockups](https://github.com/emilwallner/Screenshot-to-code-in-Keras) project from [Emil Wallner](https://github.com/emilwallner).

<b>Note:</b> This project is meant as a proof-of-concept; the model isn't (yet) built to generalize to the variability of sketches seen in actual wireframes, and thus its performance relies on wireframes resembling the core dataset.


## Setup
### Prerequisites

- Python 3 (not compatible with python 2)
- pip

### Install dependencies

```sh
pip install -r requirements.txt
```

## Example Usage

Download the data and pretrained weights:
```sh
# Getting the data, 1,700 images, 342mb
git clone https://github.com/ashnkumar/sketch-code.git
cd sketch-code
cd scripts

# Get the data and pretrained weights
sh get_data.sh
sh get_pretrained_model.sh
```

Converting an example drawn image into HTML code, using pretrained weights:
```sh
cd src

python convert_single_image.py --png_path ../examples/drawn_example1.png \
      --output_folder ./generated_html \
      --model_json_file ../bin/model_json.json \
      --model_weights_file ../bin/weights.h5
```


## General Usage

Converting a single image into HTML code, using weights:
```sh
cd src

python convert_single_image.py --png_path {path/to/img.png} \
      --output_folder {folder/to/output/html} \
      --model_json_file {path/to/model/json_file.json} \
      --model_weights_file {path/to/model/weights.h5}
```

Converting a batch of images in a folder to HTML:
```sh
cd src

python convert_batch_of_images.py --pngs_path {path/to/folder/with/pngs} \
      --output_folder {folder/to/output/html} \
      --model_json_file {path/to/model/json_file.json} \
      --model_weights_file {path/to/model/weights.h5}
```

Train the model:
```sh
cd src

# training from scratch
# <augment_training_data> adds Keras ImageDataGenerator augmentation for training images
python train.py --data_input_path {path/to/folder/with/pngs/guis} \
      --validation_split 0.2 \
      --epochs 10 \
      --model_output_path {path/to/output/model}
      --augment_training_data 1

# training starting with pretrained model
python train.py --data_input_path {path/to/folder/with/pngs/guis} \
      --validation_split 0.2 \
      --epochs 10 \
      --model_output_path {path/to/output/model} \
      --model_json_file ../bin/model_json.json \
      --model_weights_file ../bin/pretrained_weights.h5 \
      --augment_training_data 1
```

Evalute the generated prediction using the [BLEU score](https://machinelearningmastery.com/calculate-bleu-score-for-text-python/)
```sh
cd src

# evaluate single GUI prediction
python evaluate_single_gui.py --original_gui_filepath  {path/to/original/gui/file} \
      --predicted_gui_filepath {path/to/predicted/gui/file}

# training starting with pretrained model
python evaluate_batch_guis.py --original_guis_filepath  {path/to/folder/with/original/guis} \
      --predicted_guis_filepath {path/to/folder/with/predicted/guis}
```

## License

### The MIT License (MIT)

Copyright (c) 2018 Ashwin Kumar<ash.nkumar@gmail.com@gmail.com>

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
