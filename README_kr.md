# SketchCode

![](https://img.shields.io/badge/python-3-brightgreen.svg) ![](https://img.shields.io/badge/tensorflow-1.1.0-orange.svg)

*손으로 그린 와이어 프레임에서 HTML 코드 생성*

![Preview](https://github.com/ashnkumar/sketch-code/blob/master/image_for_documents/header_image.png)

SketchCode는 손으로 그린 웹 모형을 작동하는 HTML 코드로 변환하는 딥 러닝 모델입니다. [이미지 캡션](https://towardsdatascience.com/image-captioning-in-deep-learning-9cd23fb4d8d2) 아키텍처를 사용하여 손으로 그린 웹 사이트 와이어 프레임에서 HTML 마크업을 생성합니다.

자세한 내용은 다음 게시물을 참조하십시오. : [딥 러닝을 통한 프런트 엔드 개발 자동화](https://blog.insightdatascience.com/automated-front-end-development-using-deep-learning-3169dd086e82)

이 프로젝트는 [Tony Beltramelli](https://github.com/tonybeltramelli)의 [pix2code](https://github.com/tonybeltramelli/pix2code)와 [Emil Wallner](https://github.com/emilwallner)의 [Design Mockups](https://github.com/emilwallner/Screenshot-to-code-in-Keras) 프로젝트에서 합성적으로 생성된 데이터 세트와 모델 아키텍처를 기반으로 합니다.

<b>참고:</b> 이 프로젝트는 개념 증명을 위한 것입니다; 이 모델은 실제 와이어 프레임에서 볼 수 있는 스케치의 가변성에 맞게 만들어지지 않았기 때문에 성능은 코어 데이터 세트와 유사한 와이어 프레임에 의존합니다.


## 설정
### 전제조건

- Python 3 (not compatible with python 2)
- pip

### Dependencies 설치

```sh
pip install -r requirements.txt
```

## 예제

데이터 및 사전 훈련된 가중치 다운로드:
```sh
# 1,700 images, 342mb의 데이터 가져오기
git clone https://github.com/ashnkumar/sketch-code.git
cd sketch-code
cd scripts

# 데이터와 사전 훈련된 가중치 가져오기
sh get_data.sh
sh get_pretrained_model.sh
```

미리 훈련된 가중치를 사용하여 예제 그림을 HTML 코드로 변환:
```sh
cd src

python convert_single_image.py --png_path ../examples/drawn_example1.png \
      --output_folder ./generated_html \
      --model_json_file ../bin/model_json.json \
      --model_weights_file ../bin/weights.h5
```


## 일반적인 사용

가중치를 사용하여 단일 이미지를 HTML 코드로 변환:
```sh
cd src

python convert_single_image.py --png_path {path/to/img.png} \
      --output_folder {folder/to/output/html} \
      --model_json_file {path/to/model/json_file.json} \
      --model_weights_file {path/to/model/weights.h5}
```

폴더의 이미지 batch를 HTML 코드로 변환:
```sh
cd src

python convert_batch_of_images.py --pngs_path {path/to/folder/with/pngs} \
      --output_folder {folder/to/output/html} \
      --model_json_file {path/to/model/json_file.json} \
      --model_weights_file {path/to/model/weights.h5}
```

모델 훈련:
```sh
cd src

# scratch를 사용하여 훈련
# <augment_training_data>는 이미지 훈련을 위한 Keras ImageDataGenerator의 augment 기능을 추가
python train.py --data_input_path {path/to/folder/with/pngs/guis} \
      --validation_split 0.2 \
      --epochs 10 \
      --model_output_path {path/to/output/model}
      --augment_training_data 1

# 사전 훈련된 모델로 훈련 시작하기
python train.py --data_input_path {path/to/folder/with/pngs/guis} \
      --validation_split 0.2 \
      --epochs 10 \
      --model_output_path {path/to/output/model} \
      --model_json_file ../bin/model_json.json \
      --model_weights_file ../bin/pretrained_weights.h5 \
      --augment_training_data 1
```

[BLEU score](https://machinelearningmastery.com/calculate-bleu-score-for-text-python/)를 사용한 예측 평가
```sh
cd src

# GUI 예측 평가
python evaluate_single_gui.py --original_gui_filepath  {path/to/original/gui/file} \
      --predicted_gui_filepath {path/to/predicted/gui/file}

# 사전 훈련된 모델로 훈련 시작하기
python evaluate_batch_guis.py --original_guis_filepath  {path/to/folder/with/original/guis} \
      --predicted_guis_filepath {path/to/folder/with/predicted/guis}
```

## 라이센스

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
