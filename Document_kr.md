# 딥 러닝을 사용한 자동화된 프런트 엔드 개발
##### SketchCode: 아이디어에서 HTML 로 5초안에 전환

![Preview](https://github.com/ashnkumar/sketch-code/raw/master/header_image.png)

*[Ashwin Kumar](https://www.linkedin.com/in/ashnkumar/)는 회계 자동화에 머신러닝을 사용하는 Y Combinator의 신생기업인 [Sway Finance](https://swayfinance.com/) 공동 설립자였습니다. 이곳 Insight에서 그는 사용자가 손으로 그린 와이어프레임으로 작동하는 HTML 웹사이트를 만들 수 있는 모델을 개발하여 디자인 설계 프로세스를 크게 가속화했습니다. 그는 현재 [Mysthic](https://www.mythic-ai.com/)의 딥러닝 과학자입니다.*

***최첨단 응용 AI 제품을 만드는 연구자와 엔지니어 모임에 가입하세요.*** *다음 Insight AI Fellowship(Silicon Valley와 New York)의 마감일은 3월 26일입니다.*


---

사용자에게 직관적이고 매력적인 경험을 제공하는 것은 모든 기업에게 중요한 목표이며 프로토타이핑, 설계 및 사용자 테스팅의 빠른 사이클에 의해 이루어지는 프로세스입니다. Facebook과 같은 대기업들은 디자인 프로세스에 모든 팀이 참여할 수 있는 큰 대역폭(번역자: 순간적으로 보낼 수 있는 데이터의 양)을 가지고 있는데, 이는 수 주가 걸릴 수 있고 여러 이해 당사자들이 참여합니다; 반면에 소기업들은 이러한 자원을 가지고 있지 않고, 그 결과 사용자 인터페이스에 어려움을 겪을 수 있습니다.

저의 목표는 최신 딥러닝 알고리즘을 사용하여 설계 워크플로우를 크게 간소화하고 모든 기업이 웹 페이지를 신속하게 만들고 테스트할 수 있도록 지원하는 것이었습니다. 

### 오늘날의 설계 워크플로우
![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image1.png "설계 워크플로우는 여러 이해 관계자를 거치게 된다.")

일반적인 설계 워크플로우는 다음과 같을 수 있습니다:
- 제품 관리자는 제품 사양 리스트를 만들기 위해 사용자 조사를 수행합니다.
- 설계자는 요구 사항들을 수용하고 품질 낮은 프로토타입을 조사하여, 결과적으로 품질이 좋은 모델을 만듭니다.
- 엔지니어는 이러한 설계를 코드로 구현하고 사용자에게 제품을 배포합니다. 

개발 주기는 병목현상의 영향으로 빠르게 변할 수도 있고 Airbnb같은 회사들은 이런 과정을 더 효율적으로 만들기 위해 [머신러닝](https://airbnb.design/sketching-interfaces/)을 사용하기 시작했습니다.

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image2.png "그림에서 코드로 변환하는 Airbnb의 내부 AI 툴 데모")

이것이 딥 러닝 지원 설계의 예시로서 유망하기는 하지만, 이 모델이 얼마나 완전하게 훈련을 받았는지, 손으로 그린 그림의 특징에 얼마나 의존하는지는 불분명합니다. 회사만의 비공개 솔루션이기 때문에 확실히 알 수 있는 방법은 없습니다. 저는 **drawing-to-code** 기술의 오픈 소스 버전을 개발자와 디자이너 커뮤니티에서 사용할 수 있도록 만들고 싶었습니다.

이상적으로, 제 모델은 웹 사이트 디자인의 간단한 손 그림 프로토타입을 가져와서 작동하는 HTML 웹 사이트로 즉시 제작할 수 있습니다.

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/header_image.png "SketchCode 모델은 와이어 프레임을 가져와서 HTML 코드를 생성합니다.")

실제로 위의 예시는 테스트 이미지에서 생성된 실제 웹 사이트 모습입니다! 제 [깃허브](https://github.com/ashnkumar/sketch-code) 페이지에서 코드를 확인할 수 있습니다.

### 이미지 캡션에서 얻은 영감
제가 해결하던 문제는 [프로그램 합성](https://en.wikipedia.org/wiki/Program_synthesis), 즉 작동하는 소스 코드를 자동적으로 생성하는 것 이었습니다. 프로그램의 합성의 많은 많은 부분이 자연어 명세(번역자: 자연언어의 문장과 모호함을 줄이기 위한 그림이나 표)나 실행추적으로 생성된 코드를 다루지만, 저는 소스 이미지(손으로 그린 와이어프레임)을 활용할 수 있었습니다.

[이미지 캡션(Image Captioning)](https://cs.stanford.edu/people/karpathy/deepimagesent/)은 머신러닝의 잘 연구된 분야입니다. 특히 소스 이미지의 내용을 설명하기 위한 훈련 모델도 있습니다.

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image3.png "이미지 캡션 모델은 소스 이미지에 대한 설명을 생성합니다.")

최근 논문인 [pix2code](https://arxiv.org/abs/1705.07962)와 Emil Wallner의 관련 [프로젝트](https://blog.floydhub.com/turning-design-mockups-into-code-with-deep-learning/?source=techstories.org)에서 영감을 얻어 저는 제 작업을 이미지 캡션으로 재구성하기로 결정했습니다. 웹사이트 와이어프레임을 입력 이미지로, 그에 상응하는 HTML 코드를 출력 텍스트로 하였습니다.

### 올바른 데이터 얻기
이미지 캡션 기술의 접근 방식을 고려했을 때, 제 이상적인 훈련 데이터 셋은 손으로 그린 와이어프레임 스케치 수 천 쌍과 그에 상응하는 HTML 코드들 이었습니다. 당연하게도, 저는 적절한 데이터 셋을 찾을 수 없었고, 작업에 필요한 데이터들을 직접 만들어야 했습니다.

저는 pix2code 논문의 [오픈 소스 데이터 셋](https://github.com/tonybeltramelli/pix2code)으로 시작했습니다. 이 데이터 셋은 합성적으로 생성된 1,750개의 웹사이트 스크린샷과 관련 소스 코드로 구성되어 있습니다.

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image4.png "생성된 웹 사이트 이미지와 소스코드 (pix2code의 데이터 셋)")

이 데이터셋은 몇 가지 흥미로운 점을 가졌습니다:
- 데이터 셋의 각 웹 사이트는 버튼, 텍스트 상자 및 div와 같은 몇가지 간단한 [Bootstrap](https://getbootstrap.com/2.3.2/) 요소의 조합으로 구성되어 있습니다. 이는 제 모델이 '어휘'로서 몇 가지 제한된 구성 요소로 웹 사이트가 제작된 다는 것을 의미하지만, 앞으로의 접근 방식은 더 많은 어휘로 만들어져야 합니다. 
- 각 예시의 소스코드는 논문 작성자가 작업을 위해 만든 [도메인별 언어(DSL)](https://en.wikipedia.org/wiki/Domain-specific_language)로 구성되어 있습니다. 각 요소는 HTML과 CSS의 한 부분에 해당하며, 컴파일러는 DSL을 HTML 코드로 변환하는데 사용됩니다. 


![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image5.png "웹 사이트를 손으로 그린 버전으로 바꾸기")

제 작업에 필요한 데이터 셋를 수정하기 위해서는 웹 사이트 이미지를 손으로 그린 것처럼 만들어야 했습니다. 저는 각 이미지를 수정하기 위해 [OpenCV](https://opencv.org/)와 파이썬의 [PIL 라이브러리](https://pillow.readthedocs.io/en/stable/)의 회색조 변환 및 음영 감지 같은 툴을 사용하였습니다.

저는 몇가지 작업을 수행하면서 끝내 원본 웹 사이트의 CSS 스타일시트를 직접 수정하기로 결정했습니다:
- 페이지 구성 요소의 테두리 반지름을 변경하여 버튼와 div의 모서리를 곡선 처리했습니다.
- 스케치와 비슷하게 테두리 두께를 조정하고 그림자를 추가했습니다.
- 글꼴을 필기체로 변경했습니다.

제 최종 파이프라인에는 한 단계 더 추가했는데, 실제 그려진 스케치의 가변성을 위해 비틀기, 이동, 회전 등을 추가하였습니다.

### 이미지 캡션 모델 아키텍처 사용하기
이제 데이터를 준비했으니 드디어 모델에 데이터를 입력할 수 있게 되었습니다!

저는 이미지 캡션에 사용되는 [모델 아키텍처](https://github.com/emilwallner/Screenshot-to-code/blob/master/README.md)를 활용했습니다. 세 가지 주요 부분으로 구성됩니다:
- CNN(Convolutional Neural Network)을 사용하여 소스 이미지에서 특징을 추출하는 컴퓨터 비전 모델
- 소스 코드 토큰의 시퀀스를 인코딩하는 GRU(Gated Recurrent Unit) 언어 모델
- 이전 두 단계의 출력을 입력으로 받아들이고 다음 시퀀스의 토큰을 예측하는 디코더 모델(GRU)

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image6.png "토큰의 시퀀스를 입력으로 사용하여 모델 훈련")

모델을 훈련시키기 위해 소스 코드를 토큰 시퀀스로 분할했습니다. 모델에 대한 단일 입력은 원본 이미지의 시퀀스 중 하나이며, 모델의 레이블은 소스 코드의 이어지는 다음 토큰입니다. 모델은 [교차 엔트로피 비용](https://en.wikipedia.org/wiki/Cross_entropy)을 손실 함수로 사용하여 모델의 다음 토큰 예측과 실제 다음 토큰을 비교합니다.

모델이 scratch로 코드를 생성하는 작업을 수행할 때 프로세스는 약간 달라집니다. 이미지는 똑같이 CNN 네트워크를 통해 처리되지만 텍스트 프로세스는 시작 시퀀스가 기반이 됩니다. 각 단계에서 시퀀스의 다음 토큰에 대한 모델의 예측이 현재 입력 시퀀스에 추가되고 새로운 입력 시퀀스로 모델에 공급됩니다. 모델이 *END* 토큰을 예측하거나 프로세스가 소스 코드 당 제한된 토큰 수에 도달할 때까지 이 작업이 반복됩니다.

모델에서 예측된 토큰 셋이 생성되면 컴파일러는 DSL 토큰을 HTML로 변환하여 어떤 브라우저에서도 렌더링할 수 있도록 합니다.

### BLEU 점수로 모델 평가하기
저는 [BLEU 점수](https://machinelearningmastery.com/calculate-bleu-score-for-text-python/)로 모델을 평가하기로 결정했습니다. 이는 기계 번역 작업에 사용되는 일반적인 측정기준으로, 동일한 입력이 주어졌을 때 기계 생성 텍스트가  인간이 생성했을 내용과 얼마나 밀접한지 측정합니다.

기본적으로 BLEU는 생성된 텍스트와 참조 텍스트의 n-gram 시퀀스를 비교하여 정확도를 측정합니다. 생성된 HTML의 실제 요소와 상대적인 위치를 고려하므로 이 프로젝트에 적합합니다.

그리고 가장 좋은 점은 -- 생성된 웹사이트를 살펴봄으로써 BLEU 점수를 실제로 볼 수 있었다는 것입니다!

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image7.png "BLEU 점수 시각화")

BLEU의 가장 높은 점수인 1.0에서는 주어진 소스 이미지와 일치하는 위치에 올바른 구성요소를 가지고 있는 반면, 낮은 점수에서는 잘못된 위치에 잘못된 요소가 배치되었습니다. 평가 셋에서 최종 모델은 0.76의 BLEU 점수를 얻었습니다.

### BONUS - 커스텀 설계
추가로 모델은 페이지의 **골격**(문서의 토큰)만 생성하므로 컴파일 과정에서 사용자 지정 CSS 계층을 추가할 수 있으며, 그 결과 웹 사이트는 다른 스타일을 가질 수 있습니다.

![Preview](https://github.com/vbnm134678/sketch-code/blob/documentation-korean-translation/image/document_image8.png "단일 그림 => 동시에 다양한 디자인을 만들어 낸다.")

이렇게 모델 생성 프로세스에서 스타일링을 분리하면 모델을 사용할 때 몇 가지 큰 이점이 있습니다.:
- SketchCode 모델을 자사 제품에 활용하고자 하는 프런트엔드 엔지니어는 해당 모델을 그대로 사용하고 회사의 스타일 가이드에 따라 단일 CSS 파일만 변경할 수 있습니다.
- 확장성이 내장되어 있습니다. 단일 소스 이미지를 사용하여 모델 출력을 5, 10, 50개의 서로 다른 미리 정의된 스타일로 즉시 컴파일할 수 있으므로 사용자는 웹 사이트의 여러 버전을 시각화하고 브라우저에서 해당 웹 사이트를 탐색할 수 있습니다.

### 결론과 향후 방향
이미지 캡션을 활용하여 SketchCode는 손으로 그린 웹 사이트 와이어프레임을 가져와서 몇 초 안에 작동하는 HTML 웹 사이트로 변환할 수 있습니다.

모델에는 몇 가지 제한 사항이 있으며, 이어지는 정보는 다음 단계에 가능한 기능입니다:

- 이 모델은 16가지의 구성요소에 대한 어휘만 훈련되었기 때문에 데이터에서 보이는 것 이외의 토큰을 예측할 수 없습니다. 다음 단계는 이미지, 드롭다운 메뉴 및 형식과 같은 더 많은 요소를 사용하여 추가적인 웹 사이트 예제를 생성하는 것입니다. [부트스트랩 구성 요소](https://getbootstrap.com/docs/4.0/components/buttons/)에서 시작하기 좋습니다.
- 실제 제작하는 웹사이트에는 더 많은 변동성이 있습니다. 이러한 변동성을 잘 반영하는 훈련 데이터 셋를 만드는 적절한 방법은 실제 웹 사이트를 스크랩하고 사이트 콘텐츠 및 HTML/CSS 코드를 캡처 하는 것입니다.
- 또한 도면에도 CSS 수정이 완전히 파악하지 못하는 변동성이 있습니다. 손으로 그린 스케치 데이터에 더 많은 변화를 생성하는 방법은 Generative Adversarial Network를 사용하여 사실적으로 보이는 웹 사이트 이미지를 만드는 것일 수 있습니다.

여러분은 이 프로젝트에 사용된 코드를 [여기](https://github.com/ashnkumar/sketch-code) GitHub 페이지에서 찾을 수 있습니다. 저는 이 프로젝트가 다음에 어디로 갈 수 있을지 기대됩니다!


###### WRITTEN BY
##### Ashwin Kumar
##### Former fintech founder @ycombinator. Startup investor and advisor.

##### Insight
##### Insight - Your bridge to a thriving career
