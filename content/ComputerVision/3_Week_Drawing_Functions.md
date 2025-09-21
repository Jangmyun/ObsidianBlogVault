---
title: "[CV] Drawing Functions"
description: Drawing lines, rectangles, circles and polygon
draft: false
tags:
  - computer_vision
---
 
# Drawing Functions

- [[#Rectangle]]
- [[#Line]]
- [[#Circle]]
- [[#Polygon]]
- [[#Text]]

---
## Rectangle

```cpp
void rectangle(Mat& img, Point pt1, Point pt2, const Scalar& color, int thickness=1, int lineType=8, int shift=0);
```

- `pt1`: 한쪽 꼭짓점 좌표
- `pt2`: `pt1` 대각선 맞은편 꼭짓점 좌표
- `color`: `Scalar` 객체를 통한 BGR 값
- `thickness`: 사각형 테두리 선의 두께
- `lineType`: 사각형 테두리를 구성하는 선을 어떤 알고리즘으로 그릴지 지정
	- `LINE_8`: 8연결성 라인 알고리즘
	- `LINE_4`: 4연결성 라인 알고리즘
	- `LINE_AA`: 안티앨리어싱 기법 적용
- `shift`: 좌표의 정밀도 (소수점 이하 정밀도를 지정)
	- $(x,y) \rightarrow (x \times 2^{-shift}, y \times 2^{-shift})$

`Rect` 객체를 사용하여 좌상단 꼭짓점 좌표와 가로세로 길이를 지정해서 그릴 수 있다.

```cpp
void rectangle(Mat& img, Rect rect, const Scalar& color, int thickness=1, int lineType=8, int shift=0);
```

`Rect` 객체는 `Rect(x_LT, y_LT, width, height)` 로 생성한다.

### Example

```cpp
void draw_rectangle() {
  Mat image = imread("lena.png");

  Rect rect = Rect(10, 10, 100, 100);
  rectangle(image, rect, Scalar(255, 0, 0), 4, 8, 0);

  imshow("image", image);
  waitKey(0);
}
```

## Line

```cpp
void line(Mat& img, Point pt1, Point pt2, const Scalar& color, int thickness=1, int lineType=8, int shift=0);
```

### Example
```cpp
void draw_line() {
  Mat image = imread("lena.png");

  Point p1(25, 25), p2(100, 50);

  line(image, p1, p2, Scalar(255, 255, 0), 3, 8, 0);
  imshow("image", image);

  waitKey(0);
}
```

## Circle

```cpp
void circle(Mat& img, Point center, int radius, const Scalar& color, int thickness=1, int lineType=8, int shift=0);
```

### Example

```cpp
void draw_circle() {
  Mat image = imread("lena.png");

  Point center(100, 100);
  circle(image, center, 30, Scalar(0, 255, 255), 3, 8, 0);

  imshow("image", image);

  waitKey(0);
}
```

## Polygon

`fillPoly()` 함수를 사용

```cpp
void fillPoly(Mat& img, const Point** pts, const int* npts, int ncontours, const Scalar& color, int lineType=8, int shift=0, Point offset=Point());
```

- `pts`: 다각형들의 꼭짓점 좌표 배열
- `npts`: 각 다각형이 몇개의 꼭짓점으로 이루어져 있는지를 담은 정수 배열
- `ncontours`: 그릴 다각형의 총 개수
- `offset`: 모든 꼭짓점 좌표에 공통으로 더해질 오프셋 값

### Example

```cpp
void draw_polygon() {
  Mat image = Mat::zeros(400, 400, CV_8UC3);
  int w = 400;

  Point trapezoid[1][4];
  trapezoid[0][0] = Point(w * 2 / 6, w / 4);
  trapezoid[0][1] = Point(w * 4 / 6, w / 4);
  trapezoid[0][2] = Point(w * 5 / 6, w * 3 / 4);
  trapezoid[0][3] = Point(w / 6, w * 3 / 4);

  const Point* ppt[1] = {trapezoid[0]};
  int npt[] = {4};

  fillPoly(image, ppt, npt, 1, Scalar(255, 255, 0), 8);
  imshow("image", image);

  waitKey(0);
}
```


## Text

`putText()` 함수를 사용

```cpp
void putText(Mat& img, const string& text, Point org, int fontFace, double fontScale, Scalar color, int thickness=1, int lineType=8, bool bottomLeftOrigin=false);
```

- `org`: 텍스트 시작될 좌하단 꼭짓점 좌표
- `fontFace`: 사용할 글꼴 종류 지정
	- `FONT_HERSHEY_SIMPLEX`
	- `FONT_HERSHEY_PLAIN`
	- `FONT_HERSHEY_COMPLEX`
	- `FONT_HERSHEY_SCRIPT_SIMPLEX`
	- 위 옵션에 `FONT_ITALIC` 조합 가능
- `fontScale`: 글자 크기를 조절하는 배율 값
- `bottomLeftOrigin`: `true`면 이미지의 원점을 좌하단으로 간주

### Example

```cpp
void draw_text() {
  Mat image = Mat::zeros(400, 600, CV_8UC3);

  int w = image.cols;
  int h = image.rows;

  putText(image, format("width: %d, height: %d", w, h), Point(50, 80),
          FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 200, 200), 4);

  imshow("image", image);

  waitKey(0);
}
```

문자열의 경우  `format()` 함수로 printf로 타입 포맷팅 할 때와 똑같은 방식으로 지정할 수 있다.

## Draw Histogram

히스토그램을 그릴 때는 **적절한 Bin의 개수, Bin의 width** 가 중요하다.

### Example

```cpp
Mat drawHistogram(Mat src) {
  Mat hist, histImage;
  // establish the number of bins
  int i, hist_w, hist_h, bin_w, histSize;

  float range[] = {0, 256};
  const float* histRange = {range};

  hist_w = 512;
  hist_h = 400;
  histSize = 256;
  bin_w = cvRound((double)hist_w / histSize);

  // draw the histogram
  histImage = Mat(hist_h, hist_w, CV_8UC3, Scalar(255, 255, 255));

  // compute the histograms
  // &src: input image, 1: #of src image, 0: #of channels numerated from 0 ~
  // channels()-1, Mat(): optional mask hist: output histogram, 1: histogram
  // dimension, &histSize: array of histogram size, &histRange: array of
  // histogram’s boundaries
  calcHist(&src, 1, 0, Mat(), hist, 1, &histSize, &histRange);

  // Fit the histogram to [0, histImage.rows]
  // hist: input Mat, hist: output Mat, 0: lower range boundary of range
  // normalization, histImage.rows: upper range boundary NORM_MINMAX:
  // normalization type, -1: when negative, the ouput array has the same type as
  // src, Mat(): optional mask
  normalize(hist, hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());

  for (i = 0; i < histSize; i++) {
    rectangle(histImage, Point(bin_w * i, hist_h),
              Point(bin_w * i + hist_w / histSize,
                    hist_h - cvRound(hist.at<float>(i))),
              Scalar(0, 0, 0), -1);
  }
  return histImage;
}
```


`cvRound()` 함수는 실수 (`double, float`)를 가장 가까운 정수 값으로 반올림하는 역할을 한다.

```cpp
int bin_w = cvRound((double)hist_w / histSize);
```

히스토그램을 그릴 `Mat`의 width를 히스토그램 **Bin 개수**로 나누어 각 Bin 하나의 width를 구한다.

예시 코드에서는 `512 / 256 = 2.0` => `2` 가 된다.

`calcHist`는 이미지의 히스토그램을 계산하는 핵심 함수로, 각 밝기에 해당하는 픽셀이 몇개인지 계산하여 그 결과를 `Mat` 객체에 저장한다.

```cpp
calcHist(&src, 1, 0, Mat(), hist, 1, &histSize, &histRange);
```

```cpp
void cv::calcHist(
    const Mat* images,
    int                 nimages,
    const int* channels,
    InputArray          mask,
    OutputArray         hist,
    int                 dims,
    const int* histSize,
    const float** ranges,
    bool                uniform = true,
    bool                accumulate = false
);
```

- `images`: 히스토그램을 계산할 원본 `Mat` 배열 (모든 `Mat` 객체는 동일한 `CV_8U..`를 가져야 함)
- `nimages`: `images` 배열의 길이(개수)
- `channels`: 계산할 채널의 인덱스를 담은 정수 배열
	- `{0}`은 그레이스케일
	- `{0,2}`는 BGR 순서로 `B`, `R` 채널 사용
- `mask`: 선택적 마스크 - 이미지 특정 부분에 대한 히스토그램만 필요할 때 사용
- `hist`: 계산된 히스토그램이 저장될 `Mat` 객체
- `dims`: 계산할 히스토그램 차원
- `histSize`: 각 차원의 Bin 구간 개수를 담은 배열
- `ranges`: 각 차원의 히스토그램 범위를 지정하는 배열
	- `{0,256}`에서 `0`은 포함되지만 `256`은 포함되지않고 `255`까지
- `uniform`: 히스토그램 Bin zmrlrk rbsdlfgkswl duqn
- `accumulate`: `hist` 배열을 0으로 초기화하지 않고 기존 값에 계산 결과를 누적

위 과정을 통해 구한 히스토그램 값이 너무 클 수 있으므로 히스토그램을 \[0,histImage.rows\] 에 맞추기 위해 `normalize()`를 사용한다.

```cpp
normalize(hist, hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());
```

```cpp
void cv::normalize(
    InputArray  src,
    InputOutputArray dst,
    double      alpha = 1,
    double      beta = 0,
    int         norm_type = NORM_L2,
    int         dtype = -1,
    InputArray  mask = noArray()
);
```

- `src`: 정규화 진행할 입력 `Mat`
- `dst`: 정규화 결과가 저장될 출력 `Mat`
- `alpha`: 정규화 하한 계수
- `beta`: 정규화 상한 계수
- `norm_type`: 적용할 정규화 알고리즘 종류
	- `NORM_MINMAX`: 배열의 모든 값이 `alpha`와 `beta` 사이의 범위에 들어가도록 선형적 조절
	- `NORM_L1`: 배열 원소들의 절댓값 합이 `alpha`가 되도록 조절
	- `NORM_L2`: 배열 원소들의 유클리드 거리 `alpha`가 되도록 조절
	- `NORM_INF`: 배열 원소들의 절댓값 중 최대값이 `alpha`가 되도록 조절
- `dtype`: dst의 데이터 타입 지정 -  `-1`로 설정하면 `src`와 동일한 데이터 타입 사용
- `mask`: 선택적 마스크



## Write an image & a video

### `imwrite`

메모리에 존재하는 `Mat` 이미지를 파일로 저장하는 함수

```cpp
void imwrite(const String& filename, InputArray img, const std::vector<int>& params = std::vector<int>());
```

- `filename`: 저장할 파일 이름
- `img`: 저장할 img 
- `params`: 저장 옵션

### `VideoWriter` 클래스

```cpp
VideoWriter::VideoWriter(const String& filename, int fourcc, double fps, Size frameSize, bool isColor = true);
```