---
title: "[CG] 가우시안 스플래팅 (Gaussian Splatting)"
description: 가우시안 스플래팅
draft: false
tags:
  - computer_graphics
  - computer_vision
---
 
# Gaussian Splatting (가우시안 스플래팅)

3D Gaussian Splatting 은 이미지 Set에서 3D 장면으로 실시간 렌더링 가능하게 만드는 기술이다.

보통 3D 복원 시에 Voxel이나 Mesh로 점과 폴리곤을 사용한다면 가우시안 스플래팅은 '가우시안' 이 들어가는 만큼 **'스플랫'** 이라고 하는 가우시안 타원체를 매우 많이 띄워서 장면을 표현한다. 
스플랫은 중앙이 진하고 가장자리로 갈수록 흐려지는 형태이다.

스플랫이 수백만개가 서로 겹쳐졌을 때 점점 흐려지는 부드러운 경계 덕분에 경계선이 보이지 않고 매끄러운 실물처럼 보이게 된다.

스플랫은 4가지 정보를 가진다.
1. 위치 (x,y,z) : 3차원 공간에서 어디에 있는지
2. 모양과 크기: 얼마나 크고 어느 방향으로 늘어났는지
3. 불투명도: 얼마나 투명한지
4. 색상: 어떤 색인지, 보는 시점에 따라 색이 어떻게 달라지는지


![[Pasted image 20260430004213.png]]
위는 3D Gaussian Splatting 과정이다.

### SfM (Structure from Motion)Points 

이미지들을 입력으로 받아서 Camera parameter와 Point Cloud (구름) 을 생성한다. ([SfM of COLMAP](https://xoft.tistory.com/88), [Structure-from-Motion Revisited 리뷰](https://velog.io/@shj4901/Structure-from-Motion-Revisited))

앞서 말한 것 처럼 SfM의 결과로
1. **Camera Parameter**: 어디서 어느 방향으로 찍었는지)
2. **Point Cloud**: 3D 공간에 사진들에서 공통적으로 보이는 코너와 특징들의 점 구름
를 생성한다.

대부분 Point-based 방법들이 MVS ([Multi-view Stereo](https://chasuyeon.tistory.com/entry/CS5670-Lecture-16-Multi-view-stereo))  를 추가적으로 요구하지만 가우시안 스플래팅에서는 필요없다.

### Initialization

SfM 에서 생성된 점 마다 해당 자리에 가우시안을 만들어 띄운다.

초기값은 아래와 같다:
1. 크기:  가장 가까운 점 3개의 평균 거리
2. 모양: **Isotropic (등방성)** 으로 시작하여 최적화 과정에서 점점 비등방성으로 발전
3. 색: **Spherical Harmonics (SF)** 계수 통해 표현
	- 초기에는 0차항만 사용하여 대략적인 색을 잡고 시점에 따라 달라지는 색을 고차항으로 높여가며 학습 진행
4. 불투명도: 일정한 값으로 초기화 -> 최적화 하며 조절


### Projection

생성된 3D 가우시안 공분산 행렬은 월드 공간에 있다. 이걸 2D 카메라가 학습하는 사진 한장의 시점으로 변환한다.
**뷰잉 변환 행렬** $W$  를 사용하여 변환한다.

카메라 좌표계로 옮긴 3D 가우시안을 2D 이미지 상에 타원 형태의 **스플랫**으로 표현한다.

$$
Σ^`=JWΣW^TJ^T
$$
$J$ 는 [야코비안 행렬](https://angeloyeo.github.io/2020/07/24/Jacobian.html) 로, 3D->2D 투영 변환이 비선형 변환이라 변환 시 모양이 어떻게 변하는지 깔끔하게 계산하기 힘들어서 **아핀 근사** 한 비율에 관한 행렬이다.

$Σ^`$ 은 이제 2D로 projection 되었으니 z축이 필요없다. 좌상단 $2 \times 2$  만 남긴다.
이 $2 \times 2$ 공분산 행렬이 스플랫의 모양,크기,방향을 결정한다.

### Differentiable Tile Rasterization

Projection 과정으로 3D 공간의 가우시안이 2D 스플랫으로 만들어 졌다. 이제 실제 픽셀의 색으로 바꾸는 과정을 거쳐야 한다.

화면을 $16 \times 16$ 픽셀 타일로 나눠 타일 단위로 작업을 수행한다.

뷰 공간 깊이 (카메라에서 얼마나 멀리 있는지) 와 타일 ID를 결합한 키를 정렬 (Radix Sort) 한다.

정렬된 순서를 기반으로 $\alpha$ - blending 을 수행한다.
각 픽셀에 대해 그 픽셀이 속한 타일의 스플랫을 가까운 것부터 차례로 확인하면서 색을 겹친다.
(셀로판지를 여러 장 겹치는 느낌)

#### 미분 가능 (Differentiable)

색을 쌓는 과정 (Rasterization) 이 미분 가능한 연산으로만 이루어져 있어서 렌더된 이미지와 실제 이미지 간 손실이 있다면 (Gradient Flow) 3D 가우시안 파라미터를 업데이트 할 수 있다

