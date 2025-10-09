---
title: "\b[CV] Image Segmentation"
description: Image Segmentation 에 대해 알아보자
draft: false
tags:
  - computer_vision
---
 
# Image_Segmentation


# Code

## Threshold operation

### threshold

```cpp
double threshold(
	InputArray src,
	OutputArray dst,
	double thresh,
	double maxval,
	int type
);
```


- `thresh`: 임계값
- `maxval`: `type`의 조건에 따라 픽셀이 임계값을 넘었을 때 할당될 값
- `type`: 임계값 적용 방식 결정
	- `THRESH_BINARY`: `thresh` 보다 크면 `maxval`로, 작거나 같으면 0으로
	- `THRESH_BINARY_INV`: `THRESH_BINARY`의 inverse
	- `THRESH_TRUNC`: `thresh`보다 크면 `thresh`값으로 바꾸고 작거나 같으면 그대로
	- `THRESH_TOZERO`: `thresh`보다 크면 그대로, 작거나 같으면 0으로
	- `THRESH_TOZERO_INV`: `THRESH_TOZERO`의 inverse

![[Screenshot 2025-10-10 at 01.42.01.png]]

#### Example

```cpp
void testThreshold() {
  Mat image = imread(
      "/Users/chu-ingyu/repos/university-study/computer_vision/1_week_dataset/"
      "lena.png");
  Mat dst;

  cvtColor(image, image, COLOR_BGR2GRAY);
  threshold(image, dst, 100, 255, THRESH_BINARY);

  imshow("dst", dst);
  imshow("image", image);
  waitKey(0);
}
```

#### result

![[Screenshot 2025-10-10 at 01.56.22.png]]


### adaptiveThreshold

```cpp
void adaptiveThreshold(
	InputArray src, 
	OutputArray dst, 
	double maxval, 
	int adaptiveMethod, 
	int thresholdType, 
	int blockSize, 
	double C
);
```

- `maxval`: 임계값을 통과한 픽셀에 적용할 값
- `adaptiveMethod`: 임계값을 계산하는 방법
	- `ADAPTIVE_THRESH_MEAN_C`
	- `ADPATIVE_THRESH_GAUSSIAN_C`
- `thresholdType`: 적용할 임계처리 방식 `THRESH_BINARY`, `THRESH_BINARY_INV`만 사용
- `blockSize`: 임계값을 계산할 때 참조할 주변 영역 크기
- `C`: `adaptiveMethod`로 계산된 평균에 뺄 값

#### Example

```cpp
void testAdaptiveThreshold() {
  Mat image = imread("lena.png");
  Mat dst;

  cvtColor(image, image, COLOR_BGR2GRAY);

  adaptiveThreshold(image, dst, 255, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 7, 10);

  imshow("dst", dst);
  imshow("image", image);
  waitKey(0);
}

```


#### Result

![[Screenshot 2025-10-10 at 02.03.41.png]]


### inRange

```cpp
void inRange(
	InputArray src,
	InputArray lowerb, 
	InputArray upperb,
	OutputArray dst
);
```

- `lowerb`: 범위의 하한값 Scalar
- `upperb`: 범위의 상한값 Scalar

#### Example

```cpp
void testInRange() {
  Mat image = imread("hand.png");
  Mat dst;

  cvtColor(image, image, COLOR_BGR2YCrCb);

  inRange(image, Scalar(0, 133, 77), Scalar(255, 173, 127), dst);

  cvtColor(image, image, COLOR_YCrCb2BGR);
  imshow("dst", dst);
  imshow("image", image);
  waitKey(0);
}
```

#### Result

![[Screenshot 2025-10-10 at 02.14.17.png]]


## Global Thresholding

### Basic method

```cpp
void testGlobalThresholding_BasicMethod() {
  Mat image, thresh;
  int thresh_T, low_cnt, high_cnt, low_sum, high_sum, i, j, th;

  // 초기 임계값과 종료 조건 설정
  thresh_T = 200;  // 임계값의 초기 추정치
  th = 10;         // 반복을 멈출 조건 (이전 임계값과 새 임계값의 차이)

  low_cnt = high_cnt = low_sum = high_sum = 0;

  image = imread("lean.png", 0);
  cout << "Initial threshold value: " << thresh_T << endl;

  // 최적의 임계값을 찾기 위한 무한 루프
  while (1) {
    // 1. 모든 픽셀을 두 그룹으로 분류
    for (j = 0; j < image.rows; j++) {
      for (i = 0; i < image.cols; i++) {
        if (image.at<uchar>(j, i) < thresh_T) {
          // 현재 임계값보다 어두운 픽셀 그룹
          low_sum += image.at<uchar>(j, i);
          low_cnt++;
        } else {
          // 현재 임계값보다 밝은 픽셀 그룹
          high_sum += image.at<uchar>(j, i);
          high_cnt++;
        }
      }
    }

    // 2. 두 그룹의 평균 밝기 계산
    int avg_low = low_sum / low_cnt;
    int avg_high = high_sum / high_cnt;

    // 3. 새로운 임계값 계산 (두 그룹 평균의 평균)
    int new_thresh_T = (avg_low + avg_high) / 2;

    // 4. 종료 조건 확인: 이전 임계값과 새 임계값의 차이가 th보다 작으면 반복
    // 종료
    if (abs(thresh_T - new_thresh_T) < th) {
      break;
    } else {
      // 임계값을 새로 계산된 값으로 업데이트하고 다음 반복 준비
      thresh_T = new_thresh_T;
      cout << "Updated threshold value: " << thresh_T << endl;
      low_cnt = high_cnt = low_sum = high_sum = 0;  // 카운터 및 합계 초기화
    }
  }

  // 5. 최종적으로 찾은 임계값으로 이진화 수행
  cout << "\nFinal threshold value: " << thresh_T << endl;
  threshold(image, thresh, thresh_T, 255, THRESH_BINARY);

  imshow("Input image", image);
  imshow("Thresholding Result", thresh);
  waitKey(0);
}
```

![[Screenshot 2025-10-10 at 02.46.05.png]]

### Otsu's Method

```cpp
void testGlobalThresholding_OtsusMethod() {
  Mat image, result;

  image = imread( "lena.png", 0);

  threshold(image, result, 0, 255, THRESH_BINARY | THRESH_OTSU);

  imshow("input", image);
  imshow("result", result);

  waitKey(0);
}
```

![[Screenshot 2025-10-10 at 02.50.16.png]]

### Otsu's algorithm 설명

픽셀의 히스토그램을 기준으로 두 개의 그룹으로 나누었을 때, 그룹 내부의 픽셀 값들이 가능한 서로 비슷하고, 두 그룹 간에 차이가 크도록 하는 임계값 T를 찾기


#### Within-class variance (클래스 내부 분산)

이미지 픽셀들을 N개 클래스로 나누었을 때 **within class variance** 는

$$
V_W = \sum_{i=0}^{N}  (W_i \times \sigma_i^2) \quad \text{where } W_i = \frac{\text{\# of pixels in class } i}{\text{total pixels}}
$$
로 정의 가능

- $W_i$: 클래스 i의 픽셀 비율 (클래스 i의 픽셀 수 / 전체 픽셀 수)
- $\sigma_i^2$ : 클래스 i 내부의 픽셀 값 분산


## Local(Adaptive) Thresholding

```cpp
void testAdaptiveThresholding() {
  Mat image, binary, adaptive_binary;
  image = imread( "lena.png", 0);

  threshold(image, binary, 150, 255, THRESH_BINARY);
  adaptiveThreshold(image, adaptive_binary, 255, ADAPTIVE_THRESH_MEAN_C,
                    THRESH_BINARY, 85, 15);

  imshow("input", image);
  imshow("binary", binary);
  imshow("adaptive binary", adaptive_binary);

  waitKey(0);
}
```


## GrabCut

### grabCut

```cpp
void grabCut(
	InputArray img, 
	InputOutputArray mask, 
	Rect rect, 
	InputOutputArray bgdModel, 
	InputOutputArray fgdModel, 
	int iterCount, 
	int mode = GC_INIT_WITH_RECT
);
```

- `mask`: background인지 foreground인지 정의한 마스크
- `rect`: foreground 객체를 포함하는 사각형
- `bgdModel`, `fgdModel`: 알고리즘이 내부적으로 GMM 정보를 저장하는데 사용
- `iterCount`: 알고리즘 반복 횟수
- `mode`: 함수가 어떻게 동작할지 결정
	- `GC_INIT_WITH_RECT`: `rect` 파라미터를 이용해 초기화 (사각형 외부는 배경, 내부는 전경 후보로)
	- `GC_INIT_WITH_MASK`: `mask`에 확실한 전경/배경을 지정

#### Example

```cpp
void testGrabCut() {
  Mat result, bgdModel, fgdModel, image, foreground;
  image = imread("dog.png");

  Rect rectangle(15, 0, 155, 240);
  grabCut(image, result, rectangle, bgdModel, fgdModel, 10, GC_INIT_WITH_RECT);
  compare(result, GC_PR_FGD, result, CMP_EQ);
  foreground = Mat(image.size(), CV_8UC3, Scalar(255, 255, 255));
  image.copyTo(foreground, result);

  imshow("origin", image);
  imshow("Result", result);
  imshow("Foreground", foreground);

  waitKey(0);
}
```