---
title: "[CV] Edge Detection과 Line Detection"
description: Edge detection과 line detection을 알아보자
draft: false
tags:
  - computer_vision
---
 
# Edge Detection

## Introduction

- Edge pixel - 이미지의 Intensity가 급격하게 변화하는 지점에 있는 픽셀
- Edge - Edge pixel의 집합

![[Screenshot 2025-10-03 at 14.56.40.png]]

### How to detect edges?

#### 1D

**1차 미분 (first derivative)** 의 크기를 사용하여 edge를 감지

![[Screenshot 2025-10-03 at 15.06.21.png]]


#### 2D

**Image gradient**를 사용하여 edge를 검출

이미지를 intensity 값을 가진 2차원 함수 $f(x,y)$ 라고 했을 때,

**Gradient**는 $f(x,y)$ 가 각 지점에서 어느 방향으로 빠르게 변하는지를 나타내는 벡터이다.

밝기 변화가 가장 심한 방향과 그 변화량을 의미한다.

$$\nabla f \equiv \text{grad}(f) = \begin{bmatrix} g_x \\ g_y \end{bmatrix} = \begin{bmatrix} \frac{\partial f}{\partial x} \\ \frac{\partial f}{\partial y} \end{bmatrix}$$

- $g_x$ = $\frac{\partial f}{\partial x}$ : x축 방향으로의 밝기 변화율 (옆 픽셀 간 밝기 차이)
- $g_y$ = $\frac{\partial f}{\partial y}$ : y축 방향으로의 밝기 변화율 (위아래 픽셀 간 밝기 차이)


이렇게 구한 **Gradient vector** 의 크기 (Magnitude) 는 밝기 변화가 얼마나 강한지를 나타낸다.

$$M(x, y) = \text{mag}(\nabla f) = \sqrt{g_x^2 + g_y^2}$$

**Gradient Magnitude**는 피타고라스 정리를 이용해 계산한다.

**Gradient Direction**은 밝기가 가장 급격하게 증가하는 방향 으로, 아크탄젠트 함수로 계산한다.

$$\alpha(x, y) = \text{tan}^{-1} \left[ \frac{g_y}{g_x} \right]$$

Gradient Vector의 방향은 Edge Direction과 수직인 관계이다.



![[Screenshot 2025-10-03 at 15.35.15.png]]


### Edge Detection 시 노이즈의 영향

이미지에 노이즈가 있으면 edge detection 시 잘못된 결과가 나올 수 있으므로 median filtering이나 average filtering으로 이미지 smoothing하는 과정이 필요

![[Screenshot 2025-10-03 at 15.41.20.png]]


### Sobel operator

이미지의 각 픽셇에서 밝기 변화의 정도를 x축, y축의 Gradient를 근사치로 계산한다.

$$g_x = \frac{\partial f(x, y)}{\partial x} \approx f(x + 1, y) - f(x, y)$$ $$g_y = \frac{\partial f(x, y)}{\partial y} \approx f(x, y + 1) - f(x, y)$$
바로 옆 픽셀이나 아래의 픽셀과의 변화를 이용해서 기울기를 구하고,

단순 차분 연산에 가중치를 줘 수평,수직 방향 edge를 검출한다.

![[Screenshot 2025-10-03 at 16.14.57.png]]

$$M(x, y) = \text{mag}(\nabla f) = \sqrt{g_x^2 + g_y^2} \approx |g_x| + |g_y|$$

두 방향의 기울기의 magnitude를 각 픽셀에 대해 피타고라스 정리로 풀기에는 연산 오버헤드가 크기 때문에 두 절댓값을 더하는 식으로 근사치를 구한다

아래는 각각 gradient 연산자만 적용, 5x5 avg 필터링 이후에 적용한 결과이다.

![[Screenshot 2025-10-03 at 16.19.44.png]]
![[Screenshot 2025-10-03 at 16.19.56.png]]


### Canny Edge Detector

#### 알고리즘

1. **Gaussian filter**를 이용해 이미지의 노이즈를 제거
2. Gradient Magnitude와 Angle을 계산
	- Sobel Edge mask를 사용한다.
3. **nonmaxima suppression** 적용
	1. $\alpha(x,y)$ 에 가장 가까운 방향 $d_k$ 를 찾는다.
	2. $M(x,y)$가 적어도 이웃한 픽셀 중 적어도 하나보다 작다면, 해당 픽셀 값을 0으로 설정
4. double tresholding, connectivity analysis
	1. $M(x,y)  \leq T_H$  : edge
	2. $M(x,y)  < T_H$  : non-edge
	3. Otherwise : undertermined -> connectivity analysis


---
# Line Detection

### Hough transform 개념

직선은 $y = ax + b$ 로 정의할 수 있다.

**Hough transform**은 이 식을 매개변수 $a$, $b$ 에 관한 식으로 변환한다 

$$
b = -ax + y
$$
이러면 $(x,y)$ 가 고정된 값일 때 이 픽셀을 통과하는 모든 가능한 직선의 매개변수 조합을 찾을 수 있다.

![[Screenshot 2025-10-03 at 19.07.16.png]]

근데 카르테시안 좌표계를 사용하면 수직선의 경우 기울기 a 가 무한대 $\infty$  가 되는 문제가 있음

실제 Hough transform은 $b = -ax + y$ 대신 극 좌표게 ($p\theta$) 표현을 사용한다.

$$
x \cos\theta + y\sin\theta = p
$$
![[Screenshot 2025-10-03 at 20.52.56.png]]


#### 알고리즘

1. edge 정보만 포함 된 binary edge 이미지를 얻는다.
2. $p\theta$  공간 분할
3. accumulator (누적기) 셀의 개수를 조사해서 픽셀이 많이 모여있는 곳을 찾는다.

![[Screenshot 2025-10-03 at 21.05.23.png]]


#### Circle detection

Hough Transform은 $g(v, c)= 0$ 같이 매개변수로 정의될 수 있는 모든 도형에 적용 가능하다.

원의 방정식은 $(x - c_x)^2 + (x-c_y)^2 = r^2$ 로 매개변수가 3개이므로 3차원 공간이 된다.


---


# Code

## Sobel Edge Detector

```cpp
void testSobelEdgeDetector() {
  Mat image;
  Mat blur, grad_x, grad_y, abs_grad_x, abs_grad_y, result;

  image = imread("lena.png", 0);
  GaussianBlur(image, blur, Size(5, 5), 5, 5, BORDER_DEFAULT);

  Sobel(blur, grad_x, CV_16S, 1, 0, 3);
  convertScaleAbs(grad_x, abs_grad_x);

  Sobel(blur, grad_y, CV_16S, 0, 1, 3);
  convertScaleAbs(grad_y, abs_grad_y);

  addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, result);

  imshow("X", abs_grad_x);
  imshow("Y", abs_grad_y);
  imshow("Input image", image);
  imshow("Sobel Edge Detector", result);

  waitKey(0);
}
```

### GaussianBlur

```cpp
void GaussianBlur(
	InputArray src, 
	OutputArray dst, 
	Size ksize, 
	double sigmaX, 
	double sigmaY = 0, 
	int borderType = BORDER_DEFAULT
);
```

- `ksize`: 가우시안 커널의 크기 `Size(width, height)`으로 지정
- `sigmaX`: X축 방향 가우시안 표준편차
- `sigmaY`: Y축 방향 가우시안 표준편차

### Sobel

```cpp
void Sobel(
	InputArray src, 
	OutputArray dst, 
	int ddepth, 
	int dx, 
	int dy, 
	int ksize = 3, 
	double scale = 1, 
	double delta = 0, 
	int borderType = BORDER_DEFAULT
);
```


- `ddepth`: 출력이미지의 데이터 타입 
	- 미분 결과가 음수 값을 가질 수 있기 때문에 `CV_8U`는 정보가 손실됨 -> `CV_16S` 사용
- `dx`: X축 방향 미분 차수
- `dy`: Y축 방향 미분 차수
- `ksize`: 소벨 커널 크기 -> 1, 3, 5, 7 중 하나

## Canny Edge Operator

```cpp
void testCannyEdgeOperator() {
  Mat image, canny;

  image = imread( "lena.png", 0);

  Canny(image, canny, 190, 200, 3);

  imshow("input", image);
  imshow("canny", canny);

  waitKey(0);
}
```

### Canny

```cpp
void Canny(
	InputArray image, 
	OutputArray edges, 
	double threshold1, 
	double threshold2, 
	int apertureSize = 3, 
	bool L2gradient = false
);
```

- `treshold1`: 하위 임계값
	- 이 값보다 gradient 크기가 낮으면 엣지 아닌 것으로 간주
- `treshold2`: 상위 임계값
	- 이 값보다 크면 무조건 엣지로 채택 (강한 엣지)
	- `thresold1`과 `2` 사이의 값은 강한 엣지와 연결돼있을 때만 엣지로 채택
- `opertureSize`: 내부적으로 gradient 계산 시 사용하는 소벨 커널 크기
- `L2gradient`: gradient 크기 계산하는 방식 선택하는 플래그
	- `false`: $L1 = | g_x | + | g_y|$ 
	- `true`: $L2 = \sqrt{g_x^2 + g_y^2}$


## HoughLines

```cpp
void testHoughLines() {
  Mat image, edge, result;
  float rho, theta, a, b, x0, y0;
  Point p1, p2;
  vector<Vec2f> lines;
  image = imread("chess_pattern.png");
  result = image.clone();

  cvtColor(image, image, COLOR_BGR2GRAY);
  Canny(image, edge, 50, 200, 3);

  HoughLines(edge, lines, 1, CV_PI / 180, 150, 0, CV_PI);

  for (int i = 0; i < lines.size(); i++) {
    rho = lines[i][0];
    theta = lines[i][1];
    a = cos(theta);
    b = sin(theta);

    x0 = a * rho;
    y0 = b * rho;

    p1 = Point(cvRound(x0 + 1000 * (-b)), cvRound(y0 + 1000 * a));
    p2 = Point(cvRound(x0 - 1000 * (-b)), cvRound(y0 - 1000 * a));

    line(result, p1, p2, Scalar(0, 0, 255), 3, 8);
  }

  imshow("input image", image);
  imshow("edge", edge);
  imshow("Hough Transform", result);

  waitKey(0);
}
```

### HoughLines

```cpp
void HoughLines(
	InputArray image, 
	OutputArray lines, 
	double rho, 
	double theta, 
	int threshold, 
	double srn = 0, 
	double stn = 0, 
	double min_theta = 0, 
	double max_theta = CV_PI
);
```

- `lines`: 검출된 직선 정보를 저장할 벡터 `vector<Vec2f>`
- `rho`: $\rho$ (거리) 값의 해상도
- `theta`: $\theta$ (각도) 값의 해상도 (라디안) `CV_PI / 180` => 각도를 1도의 정밀도로 측정
- `threshold`: 임계값
	- 허프 변환 투표 과정에서 직선으로 인정받기 위해 받아야 할 최소 득표 수
- `srn`, `srt`: 멀티 스케일 허프 변환에 사용되는 파라미터. 기본 허프변환은 `0`
- `min_theta`, `max_theta`: 검출할 직선의 최소 및 최대 각도 범위 `0` ~ `CV_PI`

## HoughLinesP

```cpp
void testHoughLinesP() {
  Mat image, edge, result;
  vector<Vec4i> lines;

  image = imread("chess_pattern.png");
  result = image.clone();
  cvtColor(image, image, COLOR_BGR2GRAY);
  Canny(image, edge, 50, 200, 3);

  HoughLinesP(edge, lines, 1, CV_PI / 180, 50, 10, 300);

  for (int i = 0; i < lines.size(); i++) {
    Vec4i l = lines[i];
    line(result, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 3, 8);
  }

  imshow("input image", image);
  imshow("edge", edge);
  imshow("Hough Transform", result);

  waitKey(0);
}
```

### HoughLinesP

```cpp
void HoughLinesP(
	InputArray image, 
	OutputArray lines, 
	double rho, 
	double theta, 
	int threshold, 
	double minLineLength = 0, 
	double maxLineGap = 0
);
```

- `lines`: 검출된 선분 정보를 저장할 벡터 `vector<Vec4i>`-> 선분의 시작점과 끝점 좌표
- `minLineLength`: 검출할 선분의 최소 길이
- `maxLineGap`: 하나의 직선으로 간주할 점들 사이의 최대 허용 간격

### HoughLines vs. HoughLinesP

#### Result

- `HoughLines()` 는 `vector<Vec2f>`,  `(rho, theta)`를 반환
	- 무한한 직선의 정보
- `HoughLinesP()` 는 `vector<Vec4i>`,  `(x1,y1), (x2,y2)`를 반환
	- 시작점과 끝점의 좌표

#### Default parameters

- `HoughLines()`: 전체적인 직선의 속성과 관련된 파라미터 (ex: 탐색할 직선의 최소/최대 각도)
- `HoughLinesP()`: 검출된 선분 자체의 속성과 관련된 파라미터 (ex: 최소 선분의 길이나 최대 허용 간격)



