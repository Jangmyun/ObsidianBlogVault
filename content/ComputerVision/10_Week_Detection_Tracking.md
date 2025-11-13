---
title: "[CV] Detection과 Tracking"
description: Object Detection과 Tracking에 대해 알아보자
draft: false
tags:
  - computer_vision
---
 
# Detection

### Computer가 객체를 detect 하도록 만드는 방법

#### Training stage

- 대량의 Object 이미지와 non-object 이미지를 수집
- Object를 Represent하기에 적합한 **Feature** 를 찾기
- Object를 분류할 **classifier/threshold** 찾기

#### Test stage

- input 이미지에서 Feature을 추출
- Trained classifier를 사용하여 Object detect

## Face Detection

### Harr-like feature

![[Pasted image 20251114050555.png]]

- 검은색 사각형 아래의 픽셀 합에서 흰색 사각형 아래의 픽셀 합을 뺀 값
- 원본 이미지의 어떤 위치와 어떤 스케일에서도 적용 가능

크기와 위치를 바꾸어 가며 많은 양의 feature을 생성하고, 사람의 얼굴을 잘 분류하는 feature들을 선택

#### Training

OpenCVdptjsms `Adaboost` (Adaptive Boosting) 이 사용됨.

- **Boosting**: weak-learner 집합이 strong-learner를 생성하는 과정
- **Adaptive**: 이미 훈련된 weak-learner들의 정확도에 따라 각 샘플의 가중치가 조정됨.


### Cascade classifier

![[Pasted image 20251114051704.png]]

여러 개의 weak-learner 를 사용하여 strong-learner 를 생성

![[Pasted image 20251114051953.png]]

각 **strong-learner가 cascade 형태로 연결**됨
- 각 strong-learner 안의 weak-learner의 개수는 단계가 지남에 따라 감소
	- Computational power를 줄이기
- 많은 non-face 영역이 제거될 수 있다.

### Integral Image

[[#Harr-like feature]]는 사각형 영역의 픽셀 합을 계산한다. 
(검은색 사각형 영역의 픽셀합-흰색 사각형 영역의 픽셀합)

![[Pasted image 20251114053135.png]]

매번 사각형 픽셀 합을 영역 내의 모든 픽셀을 순회하며 계산하는 것은 비효율적임 (픽셀수-1 번 연산 필요)

**Integral Image**를 사용하면 *3번*의 계산만 있으면 된다 (두번의 뺄셈과 한번의 덧셈)

---
# Tracking

### Introduction

#### Basic Concept

- User-interaction이나 Detection을 통해 **ROI를 선택**
- ROI를 **히스토그램이나 Feature로 표현**
- 다음 프레임에서 ROI의 best matching patch를 찾는다.
	- 프레임과 프레임 간 간격이 짧으므로 이전 ROI와 가까운 범위에서 탐색한다.

### Meanshift (평균 이동)

주어진 이산 데이터 (**Discrete data**) 로부터  밀도 함수의 최대값 (**Maxima**) 를 찾는 과정 (**iterative method**)

![[Pasted image 20251114054659.png]]

#### Histogram Back-projection (히스토그램 역투영)

![[Pasted image 20251114055041.png]]

1. ROI 선택
2. ROI를 히스토그램/feature 로 표현
3. 다음 프레임에서 ROI와 가장 잘 일치하는 패치 탐색
4. **Histogram Back-projection**
	- 이미지의 각 픽셀이 tracking 대상의 일부일 확률을 계산
5. 최대 픽셀 분포 윈도우 획득

![[Pasted image 20251114060131.png]]

### Camshift

Meanshift를 수정한 버전

검색 window의 크기가 바뀔 수 있다. (Adaptive size)

![[Pasted image 20251114061516.png]]

### Optical Flow

연속된 프레임 사이에서 픽셀이 어떻게 움직였는가?

![[Pasted image 20251114061641.png]]

#### KLT 알고리즘

- Assumption
	- Object의 Intensity는 다음 프레임에서 변하지 않고 위치만 바뀐다.
	- 한 픽셀의 움직임은 인접 픽셀들의 움직임과 비슷하다. (덩어리째로 움직인다)


위 가정을 식으로 표현했을 때

$$
I(x, y, t) = I(x + \Delta x, y + \Delta y, t + \Delta t)
$$

여기세 테일러 급수를 적용하면

$$I(x + \Delta x, y + \Delta y, t + \Delta t) = I(x, y, t) + \frac{\partial I}{\partial x}\Delta x + \frac{\partial I}{\partial y}\Delta y + \frac{\partial I}{\partial t}\Delta t$$

$I(x + \Delta x, y + \Delta y, t + \Delta t) = I(x, y, t)$ 이므로  $\frac{\partial I}{\partial x}\Delta x + \frac{\partial I}{\partial y}\Delta y + \frac{\partial I}{\partial t}\Delta t = 0$ 이 된다.

#### KLT 알고리즘 with pyramids

기존 KLT는 큰 움직임을 인식하기 어렵다.
큰 움직임을 작은 움직임으로 바꾸기 위해 피라미드 기법을 사용

![[Pasted image 20251114062515.png]]





---

# Code


## CascadeClassifier

```cpp
CascadeClassifier face_classifier;
face_classifier.load("haarcascade_frontalface_alt.xml");
```

### detectMultiScale

```cpp
void CascadeClassifier::detectMultiScale(
	InputArray image,
	vector<Rect>& objects,
	double scaleFactor = 1.1,
	int minNeighbors = 3,
	int flags = 0,
	Size minSize = Size(),
	Size maxSize = Size()
);
```

- `image`: CV_8U 타입의 그레이스케일 이미지
- `objects`: 검출된 객체들의 Rect 목록을 저장
- `scaleFactor`: 이미지 피라미드에서 각 단계마다 이미지를 축소할 비율
	- `1.1` = 10%씩 축소
- `minNeighbors`: minNeighbors 개 이상의 겹치는 사각형이 검출된 영역만 객체로 인정한다.
- `flags`: 구버전 cascade와의 호환성을 위한 플래그 (보통 0)
- `min/maxSize`: 검출할 객체의 최소/최대 크기



### Face Detection Example Code

```cpp
void testCascadeClassifier() {
  CascadeClassifier face_classifier;
  Mat frame, grayFrame;
  vector<Rect> faces;

  VideoCapture cap(0);

  if (!cap.isOpened()) {
    cout << "Could not open camera" << endl;
    return;
  }

  face_classifier.load("haarcascade_frontalface_alt.xml");

  while (true) {
    cap >> frame;

    cvtColor(frame, grayFrame, COLOR_BGR2GRAY);
    face_classifier.detectMultiScale(
        grayFrame, faces,
        1.1,          // increase search scale by 10% each pass
        3,            // merge groups of three detections
        0,            // not used for a new cascade
        Size(30, 30)  // minimum size for detection
    );
    // draw the results
    for (int i = 0; i < faces.size(); i++) {
      Point lb(faces[i].x + faces[i].width, faces[i].y + faces[i].height);
      Point tr(faces[i].x, faces[i].y);
      rectangle(frame, lb, tr, Scalar(0, 255, 0), 3, 4, 0);
    }
    // print the output
    imshow("Face Detection", frame);
    if (waitKey(33) == 27) break;  // ESC
  }
}
```

## Tracking using meanShift and camShift

### meanShift / camShift

```cpp
int meanShift(
	InputArray probImage,
	InputOutputArray window,
	TermCriteria criteria
)
```

- `probImage`: 입력 이미지 (`calcBackProject`로 생성된 흑백의 probability map)
- `window`: 이동된 창의 새 위치
- `criteria`: 알고리즘의 종료 조건

