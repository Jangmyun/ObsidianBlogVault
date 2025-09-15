---
title: "[ComSec] 보안 취약점"
description: "\b보안 취약점 관리"
draft: false
tags:
  - example-tag
---
## 보안 취약점 관리

- 미국
	- **NIST (National Institute of Standards and Technology)**
		- 사이버 보안 분야에서 표준, 가이드라인, 모범 사례를 개발하고 보급하는 역할
	- **MITRE**
		- NIST가 국립사이버보안우수센터 (**NCCoE**) 설립하고, MITRE는 이 센터를 운영하고 NIST의 임무 지원
- 한국
	- KISA

## 관리 체계 Overview, 용어

![[Screenshot 2025-09-15 at 19.39.51.png]]

### 취약점의 식별과 분류
#### CVE (Common Vulnerabilities and Exposures) 취약점 식별자

공개된 사이버 보안 취약점에 대한 ID (**CVE 식별번호**)를 부여

#### CWE (Common Weakness Enumeration) 취약점 유형 분류

취약점이 발생하는 근본적인 원인, 소프트웨어의 구조적인 약점의 종류를 분류


### 취약점 정보의 종합, 평가

#### NVD (National Vulnerability Database) 

[[#CVE (Common Vulnerabilities and Exposures) 취약점 식별자]]를 기반으로 추가적인 정보와 분석을 덧붙여 제공 


### 시스템 설정 및 취약점 자동화 검증

#### SCAP (Security Content Automation Protocol)

정보보안을 자동화하고 표준화하기 위한 프로토콜

##### CCE (Common Configuration Enumeration)

보안과 관련된 시스템 환경 설정에 대한 식별 번호

보안 관련 시스템 설정 항목을 확인하기 위해 사용

##### CPE (Common Platform Enumeration)

하드웨어, 소프트웨어, 운영체제, 응용 프로그램 등의 플랫폼 식별 체제

##### XCCDF (Extensible Configuration Checklist Description Format)

보안 검증 이후 해당 검증 결과를 표현하는 XML 기반 표준 문서 형식

보안검증 항목에 대한 내용 작성에 사용

##### OVAL (Open Vulnerability and Assessment Language)

NVD 정보를 통해 시스템의 보안설정 상태를 검사하기 위한 언어

시스템 취약성 점검에 사용

##### CVSS (Common Vulnerability Scoring System)

취약점의 위험 정도를 계산할 수 있는 프레임워크

0.0부터 10.0까지 점수를 매겨 심각성을 점수화


## NVD, CVE, CWE 관리기관

![[Screenshot 2025-09-15 at 20.31.38.png]]

MITRE 에서 **CAPEC(Common Attack Pattern Enumeration and Classification)** 도 관리



## 표준 별 관리 주체

|    약어     | 전체 이름                                                 | 관리 주체                           | 주요 역할 / 설명                        |
| :-------: | :---------------------------------------------------- | :------------------------------ | :-------------------------------- |
|  **CVE**  | Common Vulnerabilities and Exposures                  | MITRE                           | 알려진 취약점을 고유 ID로 부여하여 식별           |
|  **CWE**  | Common Weakness Enumeration                           | MITRE                           | 소프트웨어/하드웨어 보안 약점 (취약성 유형) 분류      |
| **CAPEC** | Common Attack Pattern Enumeration and Classification  | MITRE                           | 공격자가 사용하는 공격 패턴을 분류 (CWE와 연결)     |
|  **CCE**  | Common Configuration Enumeration                      | NIST + MITRE 협력                 | 시스템/소프트웨어 보안 관련 설정 항목 식별          |
|  **CPE**  | Common Platform Enumeration                           | NIST (NVD)                      | OS, 애플리케이션, 하드웨어 등 IT 제품 명명 체계    |
| **XCCDF** | Extensible Configuration Checklist Description Format | NIST (SCAP 일부)                  | 보안 정책, 체크리스트, 벤치마크 표현 (XML 기반)    |
| **OVAL**  | Open Vulnerability and Assessment Language            | MITRE 주도 → 현재 OVAL Board (커뮤니티) | 취약점 및 시스템 상태를 기술/검증하는 표준 언어       |
| **CVSS**  | Common Vulnerability Scoring System                   | FIRST                           | 취약점 심각도를 0.0~10.0으로 평가하는 스코어링 시스템 |

## CVE Process

![[Pasted image 20250915203319.png]]

1. Discover
2. Report
	1. [CVE Program Partner](https://www.cve.org/PartnerInformation/ListofPartners) 에게 보고
3. Request
	1. 취약점에 CVE ID 부여 요청
4. Reserve
	1. CVE ID 예약
5. Submit
6. Publish

## 보안 취약점 보고 과정

[[#CVE Process]] 를 거쳐 새로운 취약점이 CVE 목록에 공개되면

NVD는 이 정보를 가져와 DB에 등록

- **CVE** 정보
- **CVSS** 심각도 점수를 통해 위험도 평가
- **CWE** 취약성 유형 분류
- **CPE**로 영향을 받는 소프트웨어 목록을 상세하게 정리

### CNA (CVE Numbering Authority)

누군가 보안 취약점을 보고하면 접수, 검증하고 CVE ID 생성과 CVE Record 생성을 담당하는 기관들

[CVE Numbering Authorities (CNAs)](https://www.cve.org/ProgramOrganization/CNAs?utm_source=chatgpt.com)

### NVD elements

1. Current Description (**CVE**)
	- 해당 CVE에 대한 설명
2. Analysis Description
	- Current Description과 같은 내용.
3. Severity (**CVSS**)
	- 해당 CVE의 심각도
	- CVSS로 계산
4. Reference to Advisories, Solutions, and Tools
	- 해당 CVE와 관련된 정보를 다룬 website 링크
5. Weakness Enumeration (**CWE**)
	- 해당 CVE와 관련된 정보를 다룬 CWE
6. Known Affected Software Configurations (**CPE**)
	- CPE(Common Platform Enumeration) 를 사용하여 분석 시 취약한 것으로 간주되는 소프트웨어 또는 소프트웨어 조합을 표시
7. Configurations
	- 분석 당시 취약한 것으로 간주되는 소프트웨어 또는 소프트웨어 조합을 보여줌
8. Change History
	- 수정 이력


### CWE

**Common Weakness Enumeration**

**CVE**를 설명할 수 있는 취약점 카테고리

#### 주요 카테고리

- Relationships
- Observed Examples (CVE)
- Demonstrative Examples
- Detection Methods
- Related Attack Patterns (CAPEC)

#### CWE-Relationships section

CWE 사이의 관계 표시

ChildOf, ParentOf, MemberOf, PeerOf 등 다양한 관계 존재

![[Screenshot 2025-09-15 at 21.11.47.png]]

#### CWE-Observed Examples (CVE)

해당 CWE가 발견되는 CVE ID 리스트 제공

각 CVE 간단한 설명 제시

#### CWE-Demonstrative Examples

실제 CWE가 발견되는 코드 예시

코드에 대한 간단한 설명 제공

#### CWE-Detection Methods

해당 CWE 검출방법 설명

#### CWE-Related Attack Patterns

관련된 **CAPEC-ID** 와 이름 제시

하나의 CWE에 관련되는 여러개 **CAPEC** 존재 가능


