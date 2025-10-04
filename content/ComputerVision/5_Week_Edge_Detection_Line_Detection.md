---
title: Edge Detection과 Line Detection
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

