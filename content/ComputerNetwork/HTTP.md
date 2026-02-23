---
title: 컴퓨터 네트워크 - HTTP (Hypertext Transfer Protocol)
description: HTTP란????
draft: false
tags:
  - computer_network
  - web
  - network
---
 
# HTTP (Hypertext Transfer Protocol)

**WWW (World Wide Web)** 에서 데이터를 주고받는 데 사용되는 통신 규약
웹 브라우저가 웹 서버에 HTML문서, 이미지, 동영상 등 정보를 **요청**하고, 서버가 그 요청에 **응답**하여 콘텐츠를 전달

## HTTP란

### HTTP 주요 특징

- 클라이언트-서버 모델
	- Req 보내는 클라이언트와 Req에 Res하는 서버 간 통신으로 구성
- **비연결성 (Stateless)** 
	- 각 요청과 응답이 독립적으로 이루어짐
	- 서버는 이전에 보낸 클라이언트의 상태를 기억하지 않음
	- 로그인 등 기능은 쿠키나 세션 같은 기술로 극복
- 메시지 형식
	- Req 메시지: 시작 줄(요청 메서드, URL, HTTP 버전), 헤더, 본문으로 구성
	- Res 메시지: 시작 줄(HTTP 버전, 상태코드, 상태 메시지), 헤더, 본문으로 구성

### HTTP 메서드

HTTP는 클라이언트가 서버에 원하는 동작을 알리기 위해 **메서드**를 사용

- **GET**
	- 서버로부터 데이터 조회
	- URL에 데이터를 포함 (보안 취약)
- **POST**
	- 서버에 새로운 리소스를 생성하거나 데이터 전송에 사용
	- 데이터를 메시지 본문에 담아 전송 (GET보다 안전)
- **PUT**
	- 서버의 기존 리소스를 수정하거나 대체
- **DELETE**
	- 서버의 특정 리소스를 삭제
- **HEAD**
	- GET과 유사하지만 메시지 본문 말고 헤더 정보만 조회
- **OPTIONS**
	- 서버가 지원하는 메서드 종류 확인

### HTTP 상태 코드

서버는 클라이언트 요청에 대한 결과를 세자리 숫자 코드로 클라이언트에 전달

- **1XX (정보)**
	- 요청이 수신되어 처리중
- **2XX (성공)**
	- 200 OK: 요청 성공
	- 201 Created: 리소스 생성 성공
- **3XX (리다이렉션)**
	- 301 Moved Permanently: 요청한 리소스가 영구적으로 이동됨
- **4XX**
	- 400 Bad Reqest: 잘못된 문법으로 요청
	- 401 Unauthorized: 인증되지 않은 클라이언트
	- 403 Forbidden: 접근 권한 없음
	- 404 Not Found: 요청한 리소스를 찾을 수 없음
- **5XX**
	- 500 Internal Server Error: 서버 내부 오류
	- 503 Service Unavailable: 서버가 일시적으로 사용 불가 상태

---

## HTTP 메시지 구조

### HTTP Request

- **Request Line**
	- Method
	- URI
	- HTTP Version
- **Request Headers**
	- 요청에 대한 추가정보 (브라우저 종류, 데이터 형식 등)
- **Request Body**

![[Pasted image 20250811164736.png]]


### HTTP Response

- **Response Status Line**
	- HTTP Version
	- Status Code
	- Status Phrase
- **Response Headers**
	- 응답에 대한 추가 정보 (서버시간, 서버 이름 등)
- **Response Body**

![[Pasted image 20250811164716.png]]



## HTTP vs. HTTPS

**HTTPS(Hypertext Transfer Protocol Secure)** 은 HTTP에 보안기능 추가한 것

| 구분  | HTTP             | HTTPS                          |
| --- | ---------------- | ------------------------------ |
| 보안  | 암호화되지 않은 데이터를 전송 | **SSL/TLS**암호화 기술을 사용하여 데이터 보호 |
| 포트  | `80`번 포트         | `443`포트                        |

속도는 암호화 과정이 없는 HTTP가 빠를 수 밖에


## HTTP/1.1 vs. HTTP/2

### 프로토콜 구조

- HTTP/1.1
	- 요청과 응답 모두 텍스트 기반 -> 데이터 크기가 커지고 파싱 효율 낮음
- HTTP/2
	- 모든 메시지가 **[[#Binary Framing]]** 계층에서 처리되고 데이터가 **Frame** 단위로 전송
	- 통신 효율 굿, 파싱 빠름

#### Binary Framing

**Frame**이라는 최소 단위로 데이터를 주고 받음
한 프레임은 고정된 구성을 가지고 프레임 헤더와 데이터(payload)로 구성

![[Pasted image 20250811173055.png]]

##### Frame

프레임의 헤더 구조는 다음과 같다

```
 +-----------------------------------------------+
 |                 Length (24)                   |
 +---------------+---------------+---------------+
 |   Type (8)    |   Flags (8)   |
 +-+-------------+---------------+-------------------------------+
 |R|                 Stream Identifier (31)                      |
 +=+=============================================================+
 |                   Frame Payload (0...)                      ...
 +---------------------------------------------------------------+
```

| Field             | Length                           | Description                                             |
| ----------------- | -------------------------------- | ------------------------------------------------------- |
| Length            | 3 bytes                          | 페이로드의 길이 (프레임 헤더 미포함)                                   |
| Type              | 1 byte                           | 프레임의 타입 지정 (DATA, HEADERS, PRIORITY, SETTINGS 등)        |
| Flags             | 1 byte                           | 프레임 타입별 플래그 필드 END_STREAM(데이터의 끝), END_HEADERS(헤더의 끝) 등 |
| Reserved (R)      | 1 bit                            | 예약 비트로, 항상 0으로 설정하고 무시                                  |
| Stream Identifier | 4 bytes (31bits 사용하고 상위 1bit 예약) | 스트림 ID (31 bits)로 해당 프레임이 어떤 HTTP/2 스트림에 속하는지 표시        |
각 **Frame Type** 별로 Payload 구조가 다른데 이는 [RFC9113](https://datatracker.ietf.org/doc/html/rfc9113)에 정리되어 있음

### Multiplexing 및 연결 관리

- HTTP/1.1
	- 커넥션 당 요청을 한번에 하나만 순차적으로 처리
	- **Head-of-Line (HOL) Blocking** 문제 발생
		- 여러 파일 요청 시 앞의 요청이 완료돼야 다음 요청이 처리
- HTTP/2
	- 멀티플렉싱을 통해 하나의 연결로 여러 요청과 응답을 동시에 처리

![[Pasted image 20250811174647.png]]

### 헤더 압축 (Header Compression)

HTTP/1.1 에서 매 요청마다 헤더 전체를 반복 전송 하는 것에 비해

HTTP/2 는 **HPACK** 방식의 헤더 압축을 적용해서 중복되는 헤더 정보를 줄인다

#### HPACK

HTTP/2 에서 헤더 필드의 중복을 제거하고 전송 효율성을 높이기 위해 사용되는 헤더 압축 알고리즘

각 요청마다 전체 헤더 필드를 전송하지 않고 2가지 테이블을 사용한다

##### Table

1. **Static Table**
	- 미리 정의된 헤더 필드 집합, 자주 사용되는 HTTP 헤더 필드를 포함
2. **Dynamic Table**
	- 연결이 유지되는 동안 새로 전송된 헤더 필드를 저장
	- 클라이언트와 서버가 공유하면서 새로운 헤더 필드가 전송될 때마다 **Dynamic Table**에 추가됨

##### 작동 방식

- **Indexed Header Field (인덱스 참조)**
	- 정적, 동적 테이블에서 이미 존재하는 헤더 필드를 인덱스로 참조하여 전송
	- 헤더 필드 전체 재전송 대신 인덱스 번호만 전송
- **Literal Header Field**
	- 새로 추가된 헤더 필드는 리터럴 형식으로 전송
	- 헤더 필드와 값이 함께 전송, 필요에 따라 동적 테이블에 추가
- **Literal Header Field with Incremental Indexing (증분 인덱싱)**
	- 새로운 헤더 필드를 전송하고 동적 테이블에 추가
	- 이후에 동일한 헤더필드 전송시에는 인덱스로 참조
- **Literal Header Field without Indexing (인덱싱 없이 전송)**
	- 헤더필드를 전송하되 동적 테이블에 추가 x
- **Literal Header Field never Indexed (절대 인덱싱 금지)**
	- 민감한 정보 포함한 헤더 필드 전송에 사용

### 서버 푸시 (Server Push)

HTTP/1.1 의 경우 클라이언트가 필요한 리소스를 직접 요청해야 했으나

HTTP/2 에서는 **Server Push** 기능으로 서버가 클라이언트가 요청하지 않은 리소스도 미리 전송하여 렌더링 속도를 단축한다

예를들어 서버가 HTML 문서를 보내면서 클라이언트가 곧 필요로 할 JS, CSS 파일을 미리 함께 보낼 수 있음

## HTTP/3 (QUIC)

구글에서 개발한 UDP 기반의 **QUIC (Quick UDP Internet Connections)** 를 사용하여 통신하는 프로토콜

![[Pasted image 20250812143044.png]]

QUIC은 TCP, TLS, HTTP의 기능을 모두 구현한 프로토콜로

TCP 사용상 문제인 **HOLB (Head-of-Line Blocking)** 문제를 해결

UDP 사용하므로 **443** 포트 사용

### QUIC 주요 특징

#### 연결 레이턴시 최소화

TLS + TCP 에서는 TCP 연결 생성을 위한 hand-shanking 과정과 TLS를 사용한 암호화 통신까지 총 **3 RTT**가 필요하다.

QUIC 내에 TLS 인증서를 포함하므로서 최초 연결 설정 한번으로 필요한 인증 정보와 데이터를 함께 전송한다.

![[Pasted image 20250812164100.png]]

#### 연결 마이그레이션

최초 연결시에 destination 서버의 **Connection ID**를 사용해서 생성한 **Initial Key**를 사용하여 통신을 암호화

한번 연결이 성공하면 그 설정을 캐싱해놓고 다음 연결 때 hand-shanking 없이 **0-RTT**로 통신을 시작할 수 있다

와이파이 환경에서 셀룰러로 네트워크가 바뀌어도 같은 QUIC Connection ID로 연결을 계속 유지할 수 있음

#### HOLB 완전 해소

HTTP/2 의 경우 기존 HTTP/1.1 가 파이프라인으로 하나의 요청에 대해 매번 커넥션을 유지해야하는 점을 보완하여 멀티플렉싱을 통한 요청 처리 방식을 도입했다.

HTTP Application Layer에서의 HOLB는 해소됐지만, TCP 본질적으로 가지는 HOLB 문제가 여전히 존재한다.

##### 독립 스트림

HTTP/2 는 하나의 TCP 커넥션으로 데이터 병렬 전송이 가능하다. 다만 여러 프레임들이 섞여서 전송되는 중에 문제가 발생하면 이후에 상관없는 프레임들까지 지연이 발생한다.

QUIC 에서는 Application layer에서 **여러개의 독립적인 스트림**을 지원함

#### 강력한 암호화

기본적으로 QUIC 내에 TLS가 포함됨

![[Pasted image 20250812203843.png]]

##### 암호화 방식

**TLS 1.3** 을 프로토콜 자체에 내장 -> 중간 네트워크 장비가 통신 내용을 들여다보거나 조작하는 것을 차단
