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



# 가우시안 스플래팅을 사용하여 3D 물체 학습하기

실내에서 한 물체를 중심으로 카메라가 빙 돌며 촬영한 영상을 기반으로 가우시안 스플래팅을 학습한 실습 과정이다.
공식 [3D Gaussian Splatting 리포지토리](https://github.com/graphdeco-inria/gaussian-splatting)를 사용하였다.

## 환경

- OS: Windows 10
- GPU: NVIDIA RTX 3080 (CUDA 사용)
- 패키지 관리: Miniconda (Conda Powershell)
- Python: 3.10.20
- COLMAP: 공식 릴리즈 zip 파일 설치 후 환경변수 등록

## 전체 파이프라인

```
영상 촬영 → 프레임 추출 → COLMAP(SfM) → Point Cloud 생성 → 가우시안 학습 → 웹 뷰어로 확인
```

## 1단계: 환경 세팅

### COLMAP 설치

1. [COLMAP 공식 릴리즈](https://github.com/colmap/colmap/releases)에서 Windows용 zip 파일 다운로드
2. `C:\COLMAP` 에 압축 해제
3. 시스템 환경변수 `Path` 에 `C:\COLMAP\bin` 추가
4. Powershell 재시작 후 확인

```powershell
colmap --version
```

### 리포지토리 클론

```powershell
git clone https://github.com/graphdeco-inria/gaussian-splatting --recursive
cd gaussian-splatting
```

`--recursive` 옵션으로 `diff-gaussian-rasterization`, `simple-knn` 등 CUDA 기반 submodule까지 함께 받는다.

### Conda 환경 세팅

```powershell
conda create -n gaussian_splatting python=3.10.20 -y
conda activate gaussian_splatting

# PyTorch CUDA 버전 설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 나머지 의존성 설치
pip install -r requirements.txt

# CUDA submodule 설치
pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn
```

## 2단계: 영상에서 프레임 추출

촬영한 영상에서 프레임을 추출하여 `images` 폴더에 저장한다.

프레임이 너무 많으면 COLMAP 매칭이 오히려 잘 안 되므로 100~300장 정도가 적당하다고 한다.

```powershell
mkdir images
# ffmpeg으로 1초당 2프레임 추출 (영상 길이에 따라 조절)
ffmpeg -i 영상파일.mp4 -vf fps=2 images/frame_%04d.jpg
```

## 3단계: COLMAP으로 SfM 실행

### 폴더 준비

```powershell
mkdir -p output/colmap/sparse
```

### Feature Extraction

```powershell
colmap feature_extractor `
  --database_path output/colmap/database.db `
  --image_path images `
  --ImageReader.single_camera 1 `
  --ImageReader.camera_model OPENCV
```

### Feature Matching

Feature Matching은 추출된 특징점들을 사진들 간에 서로 대응시키는 단계다.
COLMAP은 여러 가지 matcher를 제공하며, **촬영 방식에 따라 적절한 matcher를 선택하는 것이 매칭 품질에 결정적인 영향을 미친다.**

#### Matcher 종류 및 선택 기준

참고: [COLMAP 공식 튜토리얼 - Feature Matching](https://colmap.github.io/tutorial.html)

**1. exhaustive_matcher**

모든 이미지 쌍을 전부 비교한다. 이미지 수가 수백 장 이하로 적을 때 가장 좋은 복원 품질을 제공한다.

```
frame_0001 ↔ frame_0002
frame_0001 ↔ frame_0003
...
frame_0002 ↔ frame_0003
...
```

- 매칭 횟수: N×(N-1)/2 쌍 (100장이면 약 5,000쌍)
- 속도: 프레임 수에 따라 기하급수적으로 느려짐
- 적합한 경우: **수백 장 이하**, 물체 주변을 돌며 찍은 영상
- 부적합한 경우: 수백 장 이상 → 수 시간 소요

```powershell
colmap exhaustive_matcher `
  --database_path output/colmap/database.db
```

**2. sequential_matcher**

파일명 순서 기준으로 연속된 프레임끼리만 매칭한다. 비디오처럼 순서대로 촬영된 이미지에 적합하다.

```
frame_0001 ↔ frame_0002 ↔ frame_0003 ↔ frame_0004 ...
```

- 매칭 횟수: N-1 쌍
- 속도: 매우 빠름
- 파일명이 반드시 순서대로 정렬되어 있어야 한다 (예: `image0001.jpg`, `image0002.jpg`)
- **Loop Detection 내장**: Vocabulary Tree 기반으로 매 N번째 프레임(`loop_detection_period`)을 시각적으로 유사한 이미지들(`loop_detection_num_images`)과 추가 매칭한다. 물체를 한 바퀴 돌았을 때 처음과 끝 프레임을 연결해주는 역할을 하지만, 기본 인접 매칭에 비해 보조적인 수준이다.
- 적합한 경우: 직선 이동 영상, 드론 영상
- 부적합한 경우: 물체 주변을 돌며 찍은 영상 → loop detection이 있어도 exhaustive에 비해 매칭률이 낮음

```powershell
colmap sequential_matcher `
  --database_path output/colmap/database.db
```

**3. vocab_tree_matcher**

사전 학습된 Vocabulary Tree로 각 이미지의 시각적 최근접 이웃을 찾아 매칭한다. Spatial Re-ranking을 통해 매칭 품질을 높인다. 수천 장 이상의 대규모 이미지 컬렉션에 권장된다.

- 속도: exhaustive보다 빠르고 대규모에서도 현실적
- 별도 vocab tree 파일 필요: [https://demuc.de/colmap/](https://demuc.de/colmap/) 에서 다운로드
- 적합한 경우: **수천 장 이상**, 넓은 실외 장면

```powershell
colmap vocab_tree_matcher `
  --database_path output/colmap/database.db `
  --VocabTreeMatching.vocab_tree_path vocab_tree.bin
```

**4. spatial_matcher**

이미지의 공간적 위치(GPS 등)를 기준으로 가까운 이미지끼리 매칭한다. EXIF에서 GPS 정보를 자동으로 추출하며, 정확한 위치 정보가 있을 때 권장된다.

- 적합한 경우: GPS 정보가 포함된 드론 영상, 실외 대규모 촬영

```powershell
colmap spatial_matcher `
  --database_path output/colmap/database.db
```

**5. transitive_matcher**

이미 존재하는 매칭 관계의 전이성을 이용한다. A↔B, B↔C 매칭이 있으면 A↔C를 직접 시도한다. 다른 matcher로 먼저 매칭한 뒤 **보완용**으로 추가 실행한다.

```powershell
colmap transitive_matcher `
  --database_path output/colmap/database.db
```

**6. custom_matcher**

매칭할 이미지 쌍을 직접 텍스트 파일로 지정한다. 특정 쌍만 매칭하고 싶을 때 사용한다.

```
# pairs.txt
image0001.jpg image0005.jpg
image0002.jpg image0006.jpg
```

```powershell
colmap matches_importer `
  --database_path output/colmap/database.db `
  --match_list_path pairs.txt
```

#### 촬영 방식별 추천 matcher (AI 추천)

| 촬영 방식                    | 추천 matcher           | 이유                   |
| ------------------------ | -------------------- | -------------------- |
| 물체 주변을 빙 돌며 촬영 (수백 장 이하) | `exhaustive_matcher` | 모든 프레임이 서로 연관, 최고 품질 |
| 직선 이동 영상, 드론 영상          | `sequential_matcher` | 인접 프레임끼리만 연관, 빠름     |
| 대규모 이미지 (수천 장 이상)        | `vocab_tree_matcher` | 유사 프레임만 효율적으로 매칭     |
| GPS 정보 포함 실외 촬영          | `spatial_matcher`    | 위치 기반 인접 이미지 매칭      |
| 매칭 보완이 필요한 경우            | `transitive_matcher` | 기존 매칭 관계 전이로 보완      |

본 실습은 물체 주변을 돌며 촬영한 영상에서 110장을 추출하였으므로 `exhaustive_matcher`를 사용한다.

```powershell
colmap exhaustive_matcher `
  --database_path output/colmap/database.db
```

### Sparse Reconstruction

SfM으로 3D Point Cloud를 생성한다.

```powershell
colmap mapper `
  --database_path output/colmap/database.db `
  --image_path images `
  --output_path output/colmap/sparse
```

완료되면 `output/colmap/sparse/0/` 아래에 `cameras.bin`, `images.bin`, `points3D.bin` 이 생성된다.

## 4단계: 가우시안 스플래팅 학습

COLMAP 결과물을 바로 입력으로 사용한다. 공식 리포지토리의 `train.py`는 COLMAP 포맷을 직접 읽는다.

```powershell
conda activate gaussian_splatting

python train.py -s output/colmap
```

주요 옵션은 아래와 같다.

```powershell
python train.py `
  -s output/colmap `      # 데이터 경로 (COLMAP sparse 결과 상위 폴더)
  -m output/model `       # 모델 저장 경로
  --iterations 30000      # 학습 반복 횟수 (기본값)
```

RTX 3080 기준 30,000 iteration에 약 10~20분 소요된다.

학습이 완료되면 `output/model/point_cloud/iteration_30000/point_cloud.ply` 파일이 생성된다. 이 `.ply` 파일이 최적화된 3D 가우시안들의 집합이다.

## 5단계: 웹 뷰어로 결과 확인

`@mkkellogg/gaussian-splats-3d` npm 라이브러리를 사용하여 브라우저에서 결과를 확인한다.

### 뷰어 세팅

```powershell
mkdir viewer
cd viewer

# 라이브러리 설치
npm install three @mkkellogg/gaussian-splats-3d
```

`point_cloud.ply` 파일을 `viewer` 폴더 안에 `scene.ply` 이름으로 복사한다.

### index.html 작성

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Gaussian Splat Viewer</title>
    <style>
      body { margin: 0; background: #000; }
      canvas { display: block; }
    </style>
  </head>
  <body>
    <script type="importmap">
      {
        "imports": {
          "three": "./node_modules/three/build/three.module.js",
          "@mkkellogg/gaussian-splats-3d": "./node_modules/@mkkellogg/gaussian-splats-3d/build/gaussian-splats-3d.module.js"
        }
      }
    </script>
    <script type="module">
      import * as GaussianSplats3D from "@mkkellogg/gaussian-splats-3d";

      const viewer = new GaussianSplats3D.Viewer({
        cameraUp: [0, -1, 0],
        initialCameraPosition: [0, 0, 3],
        initialCameraLookAt: [0, 0, 0],
      });

      viewer
        .addSplatScene("./scene.ply", {
          splatAlphaRemovalThreshold: 5,
          format: GaussianSplats3D.SceneFormat.Ply,
        })
        .then(() => {
          viewer.start();
        });
    </script>
  </body>
</html>
```

### CORS 서버 실행

브라우저에서 로컬 `.ply` 파일을 불러오려면 CORS 헤더가 필요하다. 아래 Python 스크립트로 로컬 서버를 실행한다.

```python
# server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()

    def log_message(self, format, *args):
        pass

httpd = HTTPServer(('localhost', 8000), CORSHandler)
print('Serving at http://localhost:8000')
httpd.serve_forever()
```

```powershell
python server.py
```

브라우저에서 `http://localhost:8000` 을 열면 3D로 돌아다니며 결과를 확인할 수 있다.

빈 공간의 노이즈를 제외하면 물체가 3D로 잘 복원된 것을 확인할 수 있다.

## 트러블슈팅

| 문제 | 원인 | 해결 |
|---|---|---|
| COLMAP 명령어 인식 안 됨 | 환경변수 미등록 | `C:\COLMAP\bin` 을 시스템 Path에 추가 후 Powershell 재시작 |
| COLMAP matched 이미지 수가 매우 낮음 | matcher가 맞지 않음 | 물체 주변 촬영은 `exhaustive_matcher` 사용 |
| `.ply` 파일 로드 안 됨 | CORS 정책 | `server.py` 로 CORS 헤더 포함한 로컬 서버 실행 |
| CUDA 관련 에러 | PyTorch CUDA 버전 불일치 | `cu118` 등 설치된 CUDA 버전에 맞는 PyTorch 설치 |