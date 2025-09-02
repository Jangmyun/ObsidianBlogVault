---
title: "[CV] OpenCV Basics"
description: Mat, Pixeltype, Mat copy, conversion, read, display, and resize
draft: false
tags:
  - computer_vision
---
## Basic Data Structure

### Mat

Matrix

- `Mat(int rows, int cols, int type)`
- `Mat(Size size, int type)`
- `Mat(const Mat &m)`
- `Mat(Size size, int type, const Scalar &s)`

### Pixel type

- **`CV_8U`**: 8-bit unsigned integer: uchar
- `CV_8S`: 8-bit signed integer: schar
- `CV_16U`: 16-bit unsigned integer: ushort
- `CV_16S`: 16-bit signed integer: short
- `CV_32S`: 32-bit signed integer
	- int ( -2147483648~2147483647 )
- `CV_32F`: 32-bit floating-point number
	- float ( -FLT_MAX~FLT_MAX, INF, NAN )
- `CV_64F`: 64-bit floating-point number
	- double (-DBL_MAX~ DBL_MAX, INF, NAN )
- Multi-channel array:
	- `CV_8UC3` == `CV_8U(3)`
	- `CV_64FC4` == `CV_64FC(4)`


### Matrix Declaration

```cpp
void matrix_declaration() {
  int w = 150, h = 100;
  Mat image(h, w, CV_8UC1, Scalar(255));
  cout << "Size: " << image.size().height << "," << image.size().width << endl;
  imshow("image", image);
  waitKey(0);
}
```

#### result
![[Screenshot 2025-09-02 at 23.21.25.png]]

Multi-channel 이미지를 위해서는 `Scalar` 함수를

**`Scalar(255, 0, 0)`** 과 같이 사용

🧨 색공간 순서는 **BGR** 이니 주의


## Mat Copy

### Shallow Copy (얕은 복사)

**데이터의 주소만 복사** 하는 방법

![[Screenshot 2025-09-02 at 23.40.49.png]]

위 그림에서 `cv::Mat m1`을 `m2`에 대입 (`cv::Mat m2 = m1` 혹은 `cv::Mat m2(m1)`) 하면 두 `Mat` 객체는 동일한 데이터를 가리키게 된다.
### Depp Copy (깊은 복사)

**데이터를 완전히 복사**하여 새로운 메모리 공간에 할당하는 방법
`clone()`이나 `copyTo()` 메서드를 사용한다.

![[Screenshot 2025-09-02 at 23.41.01.png]]

`cv::Mat m1` 를 `m2`로 깊은 복사 하면 두 `Mat` 객체는 **서로 독립적인** 데이터를 가지게 된다.

### example 1

```cpp
void matrix_copy() {
  Mat m1 = (Mat_<double>(3, 3) << 1, 2, 3, 4, 5, 6, 7, 8, 9);

  Mat m_shallow = m1;       // 얕은 복사
  Mat m_deep = m1.clone();  // 깊은 복사

  cout << "m1=\n" << m1 << endl << endl;
  cout << "m_shallow=\n" << m_shallow << endl << endl;
  cout << "m_deep=\n" << m_deep << endl << endl;

  // Update m1
  m1.at<double>(0, 0) = 100;

  cout << "m1=\n" << m1 << endl << endl;
  cout << "m_shallow=\n" << m_shallow << endl << endl;
  cout << "m_deep=\n" << m_deep << endl << endl;

  waitKey(0);
}
```

#### result

![[Screenshot 2025-09-02 at 23.57.10.png]]


### example 2

```cpp
void matrix_copy2() {
  Mat image = imread("img.png");

  // Mat::zeros를 통해 모든 요소가 0으로 채워진 Mat 객체 생성 (static method)
  Mat mask = Mat::zeros(image.size(), image.type());
  Mat copied;

  Rect rect = Rect(10, 10, 300, 300);  // LT(left-top) position, width, height
  rectangle(mask, rect, Scalar(255, 0, 0), -1, 8, 0);
  image.copyTo(copied, mask);

  imshow("original", image);
  imshow("copied", copied);

  waitKey(0);
}
```

#### result

![[Pasted image 20250903001416.png]]


## Mat Conversion

### convertTo

```cpp
void convertTo(OutputArray m, int rtype, double alpha=1, double beta=0);
```

- **OutputArray m**: 변환된 결과가 저장될 출력 행렬
- **int rtype**: 변환할 자료형 (`CV_8U`, `CV_32F` 등). -1이면 입력 행렬과 같은 자료형 유지
- **double alpha**: 입력 데이터에 곱할 스케일 값(기본 1)
- **double beta**: 입력 데이터에 더할 값(기본 0)

모든 element를 다음 수식으로 계산

$$
m(x,y)=saturate\_cast<rType>(α⋅(this)(x,y)+β)
$$
`this(x,y)`는 입력 행렬의 해당 위치 값

**`saturate_cast<rType>`** 은 일반 C++에서의 타입 캐스팅과 달리 변환한 값이 `rType` 범위를 벗어나면 min/max 값으로 강제함

### setTo

```cpp
void setTo(InputArray value, InputArray mask=noArray());
```

- **InputArray value**: 행렬 원소에 채워 넣을 값 (예: Scalar(0), Scalar(255, 0, 0))
- **InputArray mask**: (선택) 마스크 행렬로 true인 곳에만 값 대입

### convertScaleAbs

```cpp
void convertScaleAbs(InputArray src, OutputArray dst, double alpha=1, double beta=0);
```

- **InputArray src**: 입력 행렬
- **OutputArray dst**: 변환된 결과 행렬 (8비트)
- **double alpha**: 곱할 스케일 값 (기본 1)
- **double beta**: 더할 값 (기본 0)

### 각 함수별 차이점

| 함수명                 | 주요 기능                    | 출력 타입                | 특징 및 용도                         |
| ------------------- | ------------------------ | -------------------- | ------------------------------- |
| **convertTo**       | 자료형 변환, 픽셀 값 스케일링/쉬프트 적용 | 호출 시 지정 가능           | 타입이 변할 수 있고, 스케일과 쉬프트 적용 가능     |
| **setTo**           | 행렬 전체 또는 마스크 영역의 값 대입    | 입력 행렬과 동일            | 값 전체 초기화 또는 특정 영역 초기화 용이        |
| **convertScaleAbs** | 스케일, 쉬프트 후 절댓값 + 8비트 변환  | 항상 8비트 unsigned char | 음수 값 처리 시 사용, 에지 검출 결과 등에 주로 이용 |


### example

```cpp
void matrix_conversion() {
  Mat image = imread("img.png");

  Mat after_convertTo, after_convertScaleAbs;

  imshow("original", image);

  image.convertTo(after_convertTo, CV_16SC1);
  imshow("after_convertTo", after_convertTo);

  convertScaleAbs(image, after_convertScaleAbs, 2, 3);
  imshow("after_convertScaleAbs", after_convertScaleAbs);

  image.setTo(Scalar(0));
  imshow("after setTo", image);

  waitKey(0);
}
```

#### result

![[Screenshot 2025-09-03 at 00.38.56.png]]

## Read Image/Video

### Read an image

`imread()` 함수를 통해 이미지를 읽어 `Mat` 객체로 반환

```cpp
Mat imread(const String& filename, int flags = IMREAD_COLOR);
```

- **filename**: 읽어올 이미지 파일 경로 및 이름 (예: "image.jpg")
    
- **flags**: 이미지 로딩 방식을 지정하는 옵션값으로, 주요 옵션은 다음과 같다:
    - **IMREAD_COLOR (1)**: 컬러 이미지로 읽음 (기본값, 투명도 무시, BGR 순서)
    - **IMREAD_GRAYSCALE (0)**: 흑백 이미지로 읽음
    - **IMREAD_UNCHANGED (-1)**: 이미지 원본 그대로(알파 채널 포함) 읽음
    - **IMREAD_ANYDEPTH**: 16비트, 32비트 등 원본 이미지 깊이 무시 않고 읽음
    - **IMREAD_ANYCOLOR**: 가능한 어떤 색상으로든 읽음
    - **IMREAD_REDUCED_GRAYSCALE_2,4,8**: 이미지 크기를 1/2, 1/4, 1/8로 줄인 흑백 이미지 읽기
    - **IMREAD_REDUCED_COLOR_2,4,8**: 이미지 크기를 1/2, 1/4, 1/8로 줄인 컬러 이미지 읽기


### Read a video

`VideoCapture` 클래스를 사용

[cv::VideoCapture Class Reference](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html)

#### `VideoCapture::get(int propId)`

##### 주요 propId

|propId|설명|
|---|---|
|CAP_PROP_POS_MSEC|현재 재생 위치(밀리초)|
|CAP_PROP_POS_FRAMES|다음 프레임 인덱스(0부터 시작)|
|CAP_PROP_FRAME_WIDTH|프레임 너비|
|CAP_PROP_FRAME_HEIGHT|프레임 높이|
|CAP_PROP_FPS|프레임 속도(초당 프레임 수)|
|CAP_PROP_FRAME_COUNT|전체 프레임 수|
|CAP_PROP_FOURCC|코덱 식별 4문자 코드|
|CAP_PROP_BRIGHTNESS|카메라 이미지 밝기|
|CAP_PROP_CONTRAST|카메라 이미지 대비|
|CAP_PROP_EXPOSURE|카메라 노출|

| propId                 | 설명                             |
| ---------------------- | ------------------------------ |
| CAP_PROP_POS_MSEC      | 비디오 현재 위치(밀리초), 타임스탬프          |
| CAP_PROP_POS_FRAMES    | 다음으로 디코딩/캡처할 프레임의 0부터 시작하는 인덱스 |
| CAP_PROP_POS_AVI_RATIO | 비디오 상대 위치 (0: 시작, 1: 끝)        |
| CAP_PROP_FRAME_WIDTH   | 비디오 프레임 너비                     |
| CAP_PROP_FRAME_HEIGHT  | 비디오 프레임 높이                     |
| CAP_PROP_FPS           | 초당 프레임 수 (Frame rate)          |
| CAP_PROP_FOURCC        | 코덱 4문자 코드                      |
| CAP_PROP_FRAME_COUNT   | 비디오 파일 내 프레임 총 수               |
| CAP_PROP_FORMAT        | retrieve()가 반환하는 Mat 객체의 포맷    |
| CAP_PROP_MODE          | 백엔드별 현재 캡처 모드 값                |
| CAP_PROP_BRIGHTNESS    | 이미지 밝기 (카메라 전용)                |
| CAP_PROP_CONTRAST      | 이미지 대비 (카메라 전용)                |
| CAP_PROP_SATURATION    | 이미지 채도 (카메라 전용)                |
| CAP_PROP_HUE           | 이미지 색상 (카메라 전용)                |
| CAP_PROP_GAIN          | 이미지 게인 (카메라 전용)                |
| CAP_PROP_EXPOSURE      | 노출 (카메라 전용)                    |
| CAP_PROP_CONVERT_RGB   | RGB 변환 여부의 불리언 플래그             |
| CAP_PROP_WHITE_BALANCE | 화이트 밸런스 (현재 지원 안됨)             |
| CAP_PROP_RECTIFICATION | 스테레오 카메라의 렉티피케이션 여부            |

### Examples

#### Read a video from a file

```cpp
void read_video_from_file() {
  Mat frame;
  VideoCapture cap;
  // check if file exists. if none program ends
  if (cap.open("background.mp4") == 0) {
    cout << "no such file!" << endl;
    waitKey(0);
  }
  double fps = cap.get(CAP_PROP_FPS);
  double time_in_msec = cap.get(CAP_PROP_POS_MSEC);
  int total_frames = cap.get(CAP_PROP_FRAME_COUNT);

  cout << "FPS: " << fps << endl;
  cout << "Time in msec: " << time_in_msec << endl;
  cout << "Total frames: " << total_frames << endl;
}
```

##### result

```
FPS: 24
Time in msec: 0
Total frames: 1370
```

#### Read a video from a webcam

```cpp
void read_image_from_webcam() {
  Mat frame;
  // capture from webcam
  // whose device number=0
  VideoCapture cap(0);
}
```


## Display Image/Video 

### Display an image

```cpp
void imshow(const string &winname, InputArray mat);
```


```cpp
void display_image() {
  Mat gray_image, color_image;
  // 0 on the 2nd parameter means read img in grayscale
  gray_image = imread("lena.png", 0);
  // blank 2nd parameter means 1, which means read img in colors
  color_image = imread("lena.png");
  imshow("gray image", gray_image);
  imshow("color image", color_image);
  waitKey(0);
}
```

##### result

![[Screenshot 2025-09-03 at 01.06.13.png]]

### Display a video

```cpp
void display_video() {
  Mat frame;
  int fps;
  int delay;
  VideoCapture cap;
  // check if file exists. if none program ends
  if (cap.open("background.mp4") == 0) {
    cout << "no such file!" << endl;
    waitKey(0);
  }
  fps = cap.get(CAP_PROP_FPS);
  delay = 1000 / fps;
  while (1) {
    cap >> frame;
    if (frame.empty()) {
      cout << "end of video" << endl;
      break;
    }
    imshow("video", frame);
    waitKey(delay);
  }
}
```
#### result

![[Screenshot 2025-09-03 at 01.07.57.png]]


### waitKey

```cpp
int waitKey(int delay=0);
```

milliseconds 단위로 delay한다.

`0` 은 계속해서 대기하는 special value임.

## Resize Image/Video

```cpp
void resize_image() {
  Mat img = imread("lena.png");
  Mat resize_img;

  resize(img, resize_img, Size(200, 200));

  imshow("original image", img);
  imshow("resize image", resize_img);
  waitKey(0);
}
```

#### result

![[Screenshot 2025-09-03 at 01.15.17.png]]


