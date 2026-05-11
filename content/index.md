---
title: Jangmyun's Vault
---


### Github information

<div align="center">
	<a href="https://github.com/jangmyun">
		<img height="48" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" />
	</a>
</div>

## Skills

| 분류                | 기술                                              |
| ----------------- | ----------------------------------------------- |
| **Languages**     | Python · C++ · TypeScript · C# · Kotlin         |
| **Backend**       | FastAPI · WebSocket · MQTT · asyncio · Docker   |
| **Frontend / 3D** | Three.js · React · Unity (URP / WebGL)          |
| **CV / 3D Recon** | OpenCV · COLMAP · 3D Gaussian Splatting         |
| **Hardware**      | KiCad PCB 설계 · QMK Firmware                     |
| **DevOps**        | GitHub Actions CI/CD · Docker Compose · Alembic |

## Research

  

### Flexible Video Wall System

  

> **MCNL 학부연구실** · `2025.09 – 2026.06`

모바일 디바이스를 타일처럼 배치해 대형 디스플레이를 구성하는 시스템. WebSocket 서버와 중앙제어 GUI를 담당했습니다.

<iframe width="100%" style="aspect-ratio:16/9" src="https://www.youtube.com/embed/jF1AzXNmU-4" frameborder="0" allowfullscreen></iframe>

**담당 역할**
- ArUco 마커 3D 공간 투영: 최소제곱법(`np.linalg.lstsq`)으로 다중 마커 기준 평면 피팅 → 3D→2D 정규화 좌표 변환 파이프라인 설계
- FEC Raptor Code(C 라이브러리) 기반 UDP 비디오 스트리밍 신뢰성 확보 (블록 크기 k=32/64/128/256 설정 지원)
- FastAPI(uvicorn) + UDP Server 멀티프로세스 분리, PyQt5 관리자 GUI를 공유 이벤트 루프로 통합

**기술 스택** `Python` `FastAPI` `WebSocket` `OpenCV` `asyncio` `PyQt5` `Kotlin` `NDK`


### Operating Systems TA

> **MCNL 학부연구실** · `2026.03 – 2026.06`

Operating Systems 과목 조교로서 교육 자료 제작 및 채점 담당. OpenClaw 등 최신 AI 개발 도구의 설치·운용 방법을 정리해 문서화했습니다.

---

  

## ## Projects

  

### 3D Gaussian Splatting Pipeline

  

> **개인 프로젝트** · `2026.04.30 – 2026.05.07`

  

실사 이미지 세트에서 3D 장면을 재구성하고 브라우저에서 실시간 렌더링하는 전체 파이프라인을 혼자 구성한 프로젝트입니다.

  

**구현 내용**

- COLMAP Structure-from-Motion으로 카메라 포즈 추정

- 공식 gaussian-splatting 저장소로 3DGS 모델 학습 (RTX 3080 기준 30k iteration ≈ 10–20분)

- Three.js 기반 `.splat` 웹 뷰어 개발 (CORS 정책 대응, 드래그·줌 인터랙션)

- COLMAP matcher 5종(exhaustive / sequential / vocab_tree / spatial / transitive)을 촬영 방식별로 직접 비교·문서화

- 트러블슈팅 4건 문서화 (COLMAP 환경변수, matcher 불일치, CORS, CUDA 버전)

  

**기술 스택** `Python` `COLMAP` `3D Gaussian Splatting` `Three.js` `JavaScript`

  

[github.com/jangmyun/gaussian-splatting-exercise](https://github.com/jangmyun/gaussian-splatting-exercise)

  

---

  

### CCTV 이벤트 고가용성 MQTT 브로커

  

> **IoT 실습 교과목** · `2026.04.02 – 2026.04.20`

CCTV 이벤트 메시지를 단일 장애점 없이 전달하기 위한 분산 MQTT 브로커 시스템입니다.

**구현 내용**

- C++ 커스텀 MQTT 브로커: Active/Backup Core 이중화 + RTT 기반 릴레이 경로 자동 선택
- React + Cytoscape.js 실시간 토폴로지 시각화 대시보드 (페일오버 이벤트 시각화)
- Python pytest 통합 테스트 11개 시나리오 (e2e · failover · dedup · rtt-relay 등)
- C++ 유닛 테스트 4종 + 셸 스크립트 스모크 테스트 9종

**기술 스택** `C++` `CMake` `MQTT` `Python` `React` `Cytoscape.js` `pytest`

[github.com/jangmyun/iot_midterm_availability_mqtt](https://github.com/jangmyun/iot_midterm_availability_mqtt)

  
---

### Coding Roadmap Assistant

> **CRA (교내 동아리) 4인 팀** · `2024.12.20 – 2025.02.25`

정답 대신 학습 방향과 사고 흐름을 안내하는 AI 챗봇 VSCode 익스텐션. VS Code Marketplace에 **v2.1.0** 배포 완료.

**구현 내용**
- React Webview + TypeScript UI 개발, esbuild 번들링
- OpenAI API 연동, 프롬프트 엔지니어링으로 "힌트만 주는" 답변 구조 설계
- GitHub Actions CI/CD 파이프라인 구성, GitHub Issue/PR Template 운영
- v1.0.0 → v2.1.0 버전 이력 관리 (CHANGELOG.md)

**기술 스택** `TypeScript` `React` `VSCode Extension API` `OpenAI API` `esbuild` `GitHub Actions`

[github.com/computer-research-association/codingroadmapassistant](https://github.com/computer-research-association/codingroadmapassistant)


---
  

### Metamong — 한동대 메타버스 플랫폼

> **CRA (교내 동아리)** · `2024`

한동대학교 캠퍼스를 배경으로 한 웹 기반 메타버스 플랫폼. 서버와 Unity 클라이언트를 함께 담당했습니다.

**구현 내용**
- **백엔드**: FastAPI OAuth 인증, 사용자·팀·아바타 REST API, Colyseus TypeScript WebSocket 서버 (룸 상태 동기화), Docker Compose 컨테이너화, Alembic DB 마이그레이션 5버전
- **클라이언트**: Unity(C#) + URP 2D WebGL 빌드, `INetProvider` 인터페이스로 `NetworkCore` / `MockNetworkCore` 추상화 (의존성 역전), `AuthBridge.jslib` JS↔Unity 브릿지 구현, `RemotePlayerController`로 타 플레이어 보간 렌더링, ParrelSync 로컬 멀티플레이어 테스트

**기술 스택** `Python` `FastAPI` `Colyseus` `TypeScript` `Unity` `C#` `Docker Compose` `Alembic`

  

| 링크      |                                                                                                                              |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Backend | [github.com/computer-research-association/metamong_back](https://github.com/computer-research-association/metamong_back)     |
| Client  | [github.com/computer-research-association/metamong_client](https://github.com/computer-research-association/metamong_client) |
  

---

  
### OpenCV 영상 안정화

> **컴퓨터비전 교과목** · `2025`
  
C++ + OpenCV로 프레임 간 카메라 떨림을 제거하는 영상 안정화 알고리즘을 구현한 프로젝트입니다.

**구현 내용**
- `TransformParam` 구조체로 프레임 간 카메라 이동·회전 추적
- 궤적 누적(`cumsum`) 후 이동 평균(`smooth`) 스무딩으로 떨림 제거
- `warpAffine` + `fixBorder` 스케일 보정으로 흑색 외곽 제거

**기술 스택** `C++` `OpenCV` `CMake`

[github.com/jangmyun/cv_team1_project](https://github.com/jangmyun/cv_team1_project)

---


### Full Custom Keyboard

> **개인 프로젝트** · `2023.10 – 2023.11`
  
KiCad로 PCB를 직접 설계하고 납땜·조립 후 QMK 펌웨어를 올린 커스텀 키보드. 총 5개 제작, 개발자 친구들에게 판매.

**구현 내용**
- KiCad로 36키 ortholinear 레이아웃(owt36) PCB 설계
- SMD 부품 수동 납땜 및 조립
- QMK 펌웨어 커스터마이징 (레이어, 매크로)

**기술 스택** `KiCad` `QMK Firmware` `C`

[github.com/jangmyun/full-custom-keyboard](https://github.com/jangmyun/full-custom-keyboard)

  
---
