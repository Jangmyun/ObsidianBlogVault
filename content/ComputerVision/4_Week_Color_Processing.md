---
title: "[CV] Color Processing"
description: 색상 공간의 이해와
draft: false
tags:
  - computer_vision
---
 
# Basics of Color

![[Screenshot 2025-09-25 at 17.40.53.png]]

#### Primary Colors of Light

**R**ed, **G**reen, **B**lue  빛의 3원색 조합으로 모든 색을 만들 수 있다.

#### Secondary Colors of Light

- Magenta = R + B
- Yellow = R + G
- Cyan = G + B

#### Achromatic Color (**무채색**)

- 색이 없는 상태 (Gray Scale)
- RGB 각 성분 비율이 동일할 때 무채색이 된다.
	- ex) (100,100,100), (255,255,255)

## Color Models

### RGB

R채널, G채널, B채널로 이루어짐

각 채널마다 `[0, 255]` 범위

![[Screenshot 2025-09-25 at 19.37.03.png]]


### HSI

**Hue**채널, **Saturation**채널, **Intensity**채널로 구성

- Hue (색상): 파장에 따른 지배적인 색
- Saturation (채도): 색의 선명함, 값이 클수록 뚜렷한 색
- Intensity (명도): 밝기, 빛의 세기

HSV 모델과 유사

#### 각 채널 값의 범위

- `0 < H < 360`
- `0 < S < 1`
- `0 < V < 1`

OpenCV에서는 

- `H/2 (0 < H < 180)`
- `255*S (0 < S < 255)`
- `255*V (0 < V < 255)`


![[Screenshot 2025-09-25 at 20.00.12.png]]



### YCbCr (YUV)

- Y : 밝기
- Cb : 파란색 성분과 밝기의 차이 (B-Y)
- Cr : 붉은색 성분과 밝기의 차이 (R-Y)

![[Screenshot 2025-09-25 at 20.00.58.png]]


### Grayscale

밝기 값 채널 1개만 존재한다.

Hue, Saturation 값은 0이다.


---
# Color Image Processing

앞서 배운 [[2_Week_Intensity_Transformation]] , [[3_Week_Histogram Equalization]] 등 을 컬러 이미지에 적용하려 할때,

RGB 모델을 수정하려 하면 R, G, B 각 채널의 비율 변화로 색이 왜곡될 수 있다.

따라서 **HSI**, **YCbCr**로 색공간을 변환 후에 Intensity 채널만 따로 처리해야 한다.



## Usage of **HSI**

분리된 Intensity로 색을 유지하며 영상의 밝기만 조절 가능하다.

### Color Slicing

Hue 채널에서 특정 색 영역의 픽셀만 추출하고

다른 색은 Saturation 채널의 값을 0으로 설정하여 **원하는 색만 강조** 할 수 있다.

### Color Conversion

Hue 채널 값에 접근하여 특정 영역의 색상을 다른 색으로 변환할 수 있다.


## Pseudo Coloring

인간의 눈은 회색 음영은 30-50 단계만 구분할 수 있지만
색은 100k ~ 10m 가지까지 구분가능하다

회색 영상에 색을 입히면 훨씬 많은 정보를 확인할 수 있다.

Color Scale을 함께 포함하여 색이 어떤 의미인지 이해할 수 있도록 해야 함

## White Balancing

![[Screenshot 2025-09-25 at 20.53.05.png]]

컬러 영상의 전반적인 색 intensity를 조정해 흰색인 물체가 실제로 흰색처럼 보이게 만드는 과정

### 간단한 방법

$$

\begin{bmatrix}
R \\
G \\
B
\end{bmatrix}
=
\begin{bmatrix}
\frac{255}{R'_w} & 0 & 0 \\
0 & \frac{255}{G'_w} & 0 \\
0 & 0 & \frac{255}{B'_w}
\end{bmatrix}
\begin{bmatrix}
R' \\
G' \\
B'
\end{bmatrix}
$$

- ($R'$, $G'$, $B'$) : 화이트 밸런싱 이전 원래 값
- ($R$, $G$, $B$) : 화이트 밸런싱 이후 값
- ($R'_w$ , $G'_w$ , $B'_w$) : 흰색이라고 생각되는 기준 픽셀의 값

### Color Checker 사용

표준 색상표를 참고해서 조정할 수 있다.

### Estimate white color

이미지 속 특정 영역을 흰색이라고 가정하고 보정한다.

### Gray World Assumption

색 밸런스가 좋은 사진은 모든 픽셀 색상의 평균값이 중립 회색에 가까울 것이라는 점을 기반으로 전체 색상을 보정

