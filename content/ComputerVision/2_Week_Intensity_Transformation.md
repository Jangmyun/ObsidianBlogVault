---
title: "[CV] Intensity Transformation"
description: Example Description
draft: false
tags:
  - computer_vision
---
 
# Intensity Transformation

## 개념

### Definition

input 영상의 각 픽셀의 intensity 값을 수학적 표현을 통해 해당하는 intensity 값으로 매핑하는 과정

![[Screenshot 2025-09-11 at 00.21.39.png]]

### Example of intensity transformation

![[Screenshot 2025-09-11 at 01.05.34.png]]

### Image negatives

이미지의 intensity 값의 범위가 `[0, L-1]` 일 때, 이미지의 negative는 

$s=L−1−r$

`(s:output, r:input)`이 된다.

어두운 배경에 포함된 흰색, 회색의 디테일을 강조하는 데 유용하다

![[Screenshot 2025-09-11 at 01.09.49.png]]

### Log transformation

$s=clog(1+r)$

`(c:constant, r:input, s:output)`

`r`이 0이 될 수 있지만 `log 0`은 허용되지 않으므로 1을 더하여 계산

좁은 범위의 intensity 값을 넓은 범위 값으로 매핑한다 -> 어두운 영역의 미세한 디테일이 강조 (대비 향상)

**어두운 영역의 대비를 향상시킨다**


![[Screenshot 2025-09-11 at 01.16.14.png]]

### Power-Law (Gamma) Transformation

$s=cr^γ$

`(c:constant, s:output, r:input)`



![[Screenshot 2025-09-11 at 01.22.05.png]]

`gamma` 값에 따라 이미지의 어두운 픽셀의 범위가 확장되거나 그 반대가 된다.

![[Screenshot 2025-09-11 at 01.24.01.png]]

Gamma를 1보다 작은 값으로 설정하는 것이 input 이미지가 밝아지는 것이 아니라, 어두운 영역의 디테일을 증가시키는 것이다

### Piecewise-linear transformation (구간별 선형 변환)

transformation 함수를 더 복잡하게 구성할 수 있다.

![[Screenshot 2025-09-11 at 01.30.57.png]]

**Thresholding** (임계값)을 기준으로 두개의 선형 구간을 나누어 흑백으로만 구분할 수도 있다.

![[Screenshot 2025-09-11 at 01.28.53.png]]

### Example Results

![[Screenshot 2025-09-11 at 01.36.03.png]]


---
## 소스 코드 예제

### Pixel Access

#### operator

`image.at<DATA_TYPE>(WANT_ROW, WANT_COL)` 을 통해 원하는 픽셀에 접근할 수 있다.

```cpp
void pixel_access_by_operator() {
  Mat image, image_gray;
  int value, value_B, value_G, value_R, channels;

  image = imread("lena.png");

  image_gray = imread("lena.png",0);

  // at operator
  value = image_gray.at<uchar>(50, 100);
  cout << "value : " << value << endl;

  value_B = image.at<Vec3b>(50, 100)[0];
  value_G = image.at<Vec3b>(50, 100)[1];
  value_R = image.at<Vec3b>(50, 100)[2];
  cout << "value at (100,50): " << value_B << " " << value_G << " " << value_R
       << endl;

  waitKey(0);
}
```

#### pointer

pointer는 `at` 연산자를 사용하는 것보다 빠르다.

```cpp
void pixel_access_by_pointer() {
  Mat image = imread(
      "/Users/chu-ingyu/repos/university-study/computer_vision/1_week_dataset/"
      "lena.png");

  int value, value_B, value_G, value_R, channels;

  channels = image.channels();

  // pointer
  uchar* p;
  p = image.ptr<uchar>(50);
  value_B = p[100 * channels + 0];
  value_G = p[100 * channels + 1];
  value_R = p[100 * channels + 2];

  cout << "value at (100,50): " << value_B << " " << value_G << " " << value_R
       << endl;

  waitKey(0);
}
```

`image.ptr<uchar>(50)` 은 이미지의 50번째 행의 **시작주소**를 반환한다.

`p`가 50번째 행의 첫번째 픽셀 데이터를 가리키고 있는데,
`image`의 `channel`은 3이므로, 50번째 행에서 100번째 열을 가리키는 데이터는 `p[100 * channel]`이 될 것이고, 이 값에서 `+0, 1, 2` 한 것이 각각 `B`, `G`, `R` 값을 나타낸다.

#### data member function

`DATA_TYPE* data = (DATA_TYPE*)image.data;`

`data[WANT_ROW * image.cols + WANT_COL]`

위처럼 `data`를 원하는 타입으로 형변환 후 `ROW`와 `COL` 값으로 접근할 수 있다.


### Intensity transformation

gray-scale 이미지로 **negative**, **log**, **gamma** transformation 예제 코드를 설명

#### Image negative

```cpp
void image_negative() {
  Mat image = imread("lena.png", 0);
  Mat negative_img = image.clone();
  for (int j = 0; j < image.rows; j++)
    for (int i = 0; i < image.cols; i++)
      negative_img.at<uchar>(j, i) = 255 - image.at<uchar>(j, i);

  imshow("Input image", image);
  imshow("Negative transformation", negative_img);

  waitKey(0);
}
```

반복문으로 각 `row`와 `col`을 순회하며 `at` 연산자를 실행하여 깊은 복사를 시행한 `Mat` 객체의 값을 바꿔준다.

![[Screenshot 2025-09-11 at 02.57.53.png]]




#### Log transformation

```cpp
void log_transformation() {
  Mat image = imread("lena.png", 0);
  Mat f_img, log_img;

  double c = 1.5f;  // scale constant

  // log 계산을 위해 float 타입으로 변환
  image.convertTo(f_img, CV_32F);

  f_img = abs(f_img) + 1;  // 0 이하 값이 없도록 절댓값 처리
  log(f_img, f_img);       // 각 픽셀에 로그 연산

  // 로그 연산의 결과를 0~255 범위로 다시 맞춤
  normalize(f_img, f_img, 0, 255, NORM_MINMAX);
  convertScaleAbs(f_img, log_img,
                  c);  // scaling by c, conversion to an unsigned 8-bit type

  imshow("Input image", image);
  imshow("Log transformation", log_img);

  waitKey(0);
}
```

![[Screenshot 2025-09-11 at 03.07.35.png]]

#### Gamme Correction

```cpp
void gamma_correction() {
  Mat image = imread("lena.png", 0);
  Mat gamma_img;

  MatIterator_<uchar> it, end;

  float gamma = 0.5;
  unsigned char pix[256];

  for (int i = 0; i < 256; i++) {
    pix[i] = saturate_cast<uchar>(pow((float)(i / 255.0), gamma) * 255.0f);
  }

  gamma_img = image.clone();
  for (int j = 0; j < image.rows; j++)
    for (int i = 0; i < image.cols; i++)
      gamma_img.at<uchar>(j, i) = pix[gamma_img.at<uchar>(j, i)];

  imshow("Input image", image);
  imshow("Gamma transformation", gamma_img);

  waitKey(0);
}
```

위 예제에서는 `pix[256]` 배열을 사용해 불필요한 추가 연산없이 픽셀 값을 빠르게 변환하도록 한다.

이렇게 한 번 계산해둔 배열을 **룩업 테이블 LUT** 이라고 한다.

`0~255` 값인 `i`에 대해 `i/255.0` 연산을 통해 값의 범위를 **`0~1`로 정규화**한다.

정규화된 값에 대해 `gamma` 지수로 `pow()` 연산을 해도 여전히 값은 `0~1` 범위이다.

다시 `*255.0`으로 `0~255` 범위 값으로 되돌린다.

`saturate_cast<uchar>` 로 정수형으로 변환한다.


![[Screenshot 2025-09-11 at 03.24.14.png]]


## Spatial Filtering

이미지의 각 픽셀 값을 주변의 픽셀과 결합해서 새 값으로 매핑

이때 사용되는 필터를 spaital mask, kernel, template, window 등으로 부른다

![[Screenshot 2025-09-11 at 03.28.24.png]]![[Screenshot 2025-09-11 at 03.28.43.png]]

#### example

![[Screenshot 2025-09-11 at 03.34.51.png]]

빨간색, 파란색, 초록색 픽셀에 대해 우측 행렬을 통해 spatial filtering을 적용했을 때 값은 아래와 같다.

### Average filter

작은 **filter mask** 행렬을 각 픽셀마다 순회하며 마스크 영역 내의 모든 픽셀 강도 값의 평균을 계산하여 중심 픽셀 값을 교체한다.

**low pass filter (저역 통과 필터)**라고도 부른다.

random noise를 감소시키지만 이미지를 흐릿하게 만든다 (blur)

![[Screenshot 2025-09-11 at 03.42.13.png]]


### Gaussian filter

Gaussian function을 사용해 영상을 부드럽게 만드는 필터

![[Screenshot 2025-09-11 at 03.44.12.png]]

### Mask Size

spatial filtering을 적용할 때 mask 의 사이즈는 중요하다.

작은 물체를 블러처리 할 때는 작은 사이즈의 mask를 사용해야 한다.

mask 사이즈가 커질수록 연산 비용이 증가한다.

![[Screenshot 2025-09-11 at 03.47.38.png]]


### Sharpening

sharpening은 영상의 **intensity 변화를 강조**한다.

**Spatial differentiation (공간 미분)**을 통해 수행한다.

![[Screenshot 2025-09-11 at 03.48.12.png]]

Sharpening은 영상의 intensity 변화를 측정한다고 했다.

![[Screenshot 2025-09-11 at 03.52.12.png]]

**second derivative (2차 미분)**을 이용해 강도가 급격하게 변하는 edge, line 부분을 찾아낸다.

Sharpening 의 과정은 다음과 같다

1. Input 영상의 second derivative 값을 계산
2. second derivative 값을 input 이미지에 더하기


![[Screenshot 2025-09-11 at 03.57.40.png]]

#### sharpening using unsharp masking

![[Screenshot 2025-09-11 at 03.59.25.png]]

### Median filter

#### Median value

`3X3` 에서 중앙값은 5번째로 큰 값이고, `5X5` 에서 중앙은 13번째로 큰 값이다.

마스크 영역 내의 모든 픽셀 값을 크기 순으로 정렬하고 중앙값으로 중심 픽셀의 값을 대체한다.

![[Screenshot 2025-09-11 at 04.03.14.png]]