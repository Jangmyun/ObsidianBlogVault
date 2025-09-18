---
title: "[CV] Histogram Equalization"
description: Histogram Equalization과 예제 코드
draft: false
tags:
  - computer_vision
---


## Definition of a histogram

이미지 히스토그램은 각 intensity level을 하나의 bin으로 보고, 해당 intensity value를 가진 픽셀이 이미지 전체에 몇 개나 있는지를 세어 그래프로 나타냄

$$h(r_k) = n_k$$

- $r_k$ : 이미지의 k번째 밝기 값 (intensity value)
- $n_k$ : 이미지 전체에서 intensity level이 **$r_k$인 픽셀의 총 개수
- $L$ : 이미지에서 표현 가능한 총 밝기 단계의 수
	- $L = 2^8 = 256$


![[Screenshot 2025-09-17 at 22.20.45.png]]

### Cumulative histogram

특정 밝기 값까지의 픽셀 개수를 모두 더해, 픽셀 개수를 모두 더해 픽셀 수가 어떻게 누적되는지를 보여주는 그래프

### Histogram normalization

각 밝기의 픽셀 수를 전체 픽셀 수로 나누어 해당 intensity value가 나타날 확률을 나타낸 그래프

### Histogram 예제

![[Screenshot 2025-09-17 at 22.38.26.png]]

- Intensity level = 16 \[0,15\]
- Number of bins = 4
	- 1 bin\[0-13\] : 28/30
	- 2 bin\[4-7\] : 1/30
	- 3 bin\[8-11\] : 1/30
	- 4 bin\[12-15\] : 0/30



## Histogram equalization

픽셀 값의 분포를 조정하여 이미지의 대비를 조절

![[Screenshot 2025-09-18 at 00.36.47.png]]

#### 1. Histogram Computation

#### 2. Find Mapping Function

#### 3. Apply Mapping Function


### 예제 코드

```cpp
void histogram_equalization() {
  Mat image = imread("lena.png", 0);
  if (!image.data) exit(1);
  Mat histogram_equalized_image;

  equalizeHist(image, histogram_equalized_image);  // histogram equalization

  imshow("original", image);
  imshow("equalizeHist", histogram_equalized_image);

  waitKey(0);
}
```