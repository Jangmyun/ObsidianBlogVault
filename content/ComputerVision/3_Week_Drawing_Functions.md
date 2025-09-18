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

```cpp
void fillPoly(Mat& img, const Point** pts, const int* npts, int ncontours, const Scalar& color, int lineType=8, int shift=0, Point offset=Point());
```

- `pts`: 다각형들의 꼭짓점 좌표 배열
- `npts`: 각 다각형이 몇개의 꼭짓점으로 이루어져 있는지를 담은 정수 배열
- `ncontours`: 그릴 다각형의 총 개수
- `offset`: 모든 꼭짓점 좌표에 공통으로 더해질 오프셋 값


## Text

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

