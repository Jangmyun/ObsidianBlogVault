---
title: "[CV] Image Feature Matching"
description: Feature matching에 대해 알아보자
draft: false
tags:
  - computer_vision
---
 
# Image Feature Matching

Image Feature 란 특정 어플리케이션과 관련된 계산 작업을 해결하는 데 더 **적합한 정보 조각**을 의미한다.

### 좋은 Feature란

- 조명 (Illumination)
- 이동 (Translation)
- 스케일 (Scale)
- 회전 (Rotation)
- 원근 변환 (Perspective transform)

에 대해 **불변 (invariant)** 해야 한다.

또 **Computationally inexpensive (계산 비용이 저렴)** 하고, **Memory efficient (메모리 효율적)** 이어야 한다.

## ORB

oFast detector + r-BRIEF descriptor

### FAST

N개 이상의 연속된 픽셀의 intensity가 중앙 픽셀의 강도보다 높거나 낮을 때 코너로 판별한다.

![[Pasted image 20251114010611.png]]

### BRIEF

binary intensity test set 으로부터 구성된 이미지 패치의 **bit string descriptor**

![[Pasted image 20251114011215.png]]

feature 점 주변에 무작위 픽셀 x, y 쌍을 선택해서 두 픽셀의 intensity를 비교해서 x가 y보다 작으면 1 아니면 0

ORB는 빠르고, **illumination과 rotation에 대해 invariant**를 갖는다

## Image matching

1. **Feature Extractor**를 사용하여 input 이미지로부터 feature 찾기
2. **Feature Descriptor**를 사용하여 각 feature를 describe
3. input 이미지와 feature 사이의 유사성을 비교
4. "Good Matching"을 추출

### Good Matching

두 특징 A와 B 사이가 좋은 매칭이라면 오직 A와 B만이 서로 유사해야 한다.

**NNDR**을 사용하여 Good Matching을 추정할 수 있다.

### NNDR

$$
NNDR\;(Nearest\; neighbor\; distance\; ratio) = \frac{distance\;to\;best\;match}{distance\;to\;second\;best\;match}
$$

NNDR이 0에 가까울수록 (가장 좋은 매칭이 두번째로 좋은 매칭보다 훨씬 좋을수록) 좋은 매칭

## Convolutional Neural Network (CNN)

![[Pasted image 20251114014914.png]]

### Convolution

spatial filtering과 비슷하게 커널을 연산하면 된다.

이때 **Stride** 는 커널이  input image를 지나갈 때 한번에 몇 픽셀씩 건너뛸지를 결정한다.

![[Pasted image 20251114014941.png]]

아래 예시처럼 4x4 결과를 가지기 위해 input 이미지에 **padding**을 붙일 수 있다.

### Relu

![[Pasted image 20251114021134.png]]

일종의 non-linear (비선형) 함수로,

CNN의 계산 결과가 양수일때만 통과시키고 음수일때는 통과하지 않는다.

이를 통해 이미지의 비선형성을 증가시킨다.

### Pooling

[[#Convolution]] 연산을 통과한 Feature map의 크기를 줄이는 과정 (다운 샘플링)

![[Pasted image 20251114021735.png]]

위 예시는 Max Pooling 과정으로, 2x2 filter 필터를 사용하여 해당 영역에서 가장 큰 값을 선택한다.


---

## Code

### drawMatches
```cpp
void cv::drawMatches(
	InputArray img1,
	const std::vector<KeyPoint>& keypoints1,
	InputArray img2,
	const std::vector<KeyPoint>& keypoints2,
	const std::vector<DMatch>& matches1to2,
	InputOutputArray outImg,
	const Scalar & matchColor = Scalar::all(-1),
	const Scalar & singlePointColor = Scalar::all(-1),
	const std::vector<char>& matchesMask = std::vector<char>(),
	int flags = DrawMatchesFlags::DEFAULT
)
```

- `img1`: 왼쪽에 그려질 이미지
- `keypoints1`: `img1`에서 검출된 KeyPoint 벡터
- `img2`: 오른쪽에 그려질 이미지
- `keypoints2`: `img2`에서 검출된 KeyPoint 벡터
- `matches1to2`: 두 이미지 간 매칭 정보가 담긴 DMatch 벡터
- `outImg`: 두 이미지가 나란히 붙고 매칭 결과가 그려질 최종 출력 이미지
- `matchColor`: 매칭에 성공한 KeyPoint와 그 사이를 잇는 선의 색상
	- `Scalar::all(-1)`: 각 매칭마다 랜덤 색상으로 지정
- `singlePointColor`: 매칭에 실패한 단일 KeyPoint를 그릴 색상
- `matchesMask`: 어떤 matches를 그릴지 정하는 마스크
- `flags`: 그리기 옵션을 지정
	- `DrawMatchesFlags::DEFAULT`: 매칭에 실패한 점과 성공한 점 모두 그림
	- `DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS`: 실패는 그리지 않음


```cpp
#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main() {
  Mat query, image, descriptors1, descriptors2;

  Ptr<ORB> orbF = ORB::create(1000);
  vector<KeyPoint> keypoints1, keypoints2;
  vector<vector<DMatch>> matches;  // descriptor match
  vector<DMatch> goodMatches;
  BFMatcher matcher(NORM_HAMMING);
  Mat imgMatches;

  int i, k;
  float nndr;

  query = imread("query.jpg");
  image = imread("input.jpg");

  if (query.empty() || image.empty()) return -1;

  // Compute ORB Features
  orbF->detectAndCompute(query, noArray(), keypoints1, descriptors1);
  orbF->detectAndCompute(image, noArray(), keypoints2, descriptors2);

  // KNN Matching (k-nearest neighbor matching)
  // Find best and second-best matches
  k = 2;
  matcher.knnMatch(descriptors1, descriptors2, matches, k);

  // Find out the best match is definitely better than the second-best match
  nndr = 0.6f;  // NNDR 값이 0에 가까울수록 good matching 이다.
  for (i = 0; i < matches.size(); ++i) {
    if (matches.at(i).size() == 2 &&
        matches.at(i).at(0).distance <= nndr * matches.at(i).at(1).distance) {
      goodMatches.push_back(matches[i][0]);
    }
  }

  drawMatches(query, keypoints1, image, keypoints2, goodMatches, imgMatches,
              Scalar::all(-1), Scalar(-1), vector<char>(),
              DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);

  if (goodMatches.size() < 4) {
    cout << "Matching failed" << endl;
    return 0;
  }

  imshow("imgMatches", imgMatches);
  waitKey(0);

  return 0;
}
```



