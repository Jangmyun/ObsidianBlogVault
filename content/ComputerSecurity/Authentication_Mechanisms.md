---
title: User Authentication Mechanisms
description: 유저 인증 메커니즘에 대해 알아보자
draft: true
tags:
  - computer_security
---
 
## Authentication

어떤 것의 **신원이 확립되는 과정**

- 사용자나 자원을 식별 (identify) 하고
- 통신이 이루어지기 전에 신뢰를 설정
- 개인이 주장하는 신원을 **Verification** 하거나 **Identification**하는 과정

### Identification (식별)

"claimant가 등록된 사용자인가, 그 사용자는 누구인가?"

**one-to-many** 비교 -> 데이터베이스의 여러 사용자 정보와 비교해서 일치하는 사용자 찾기

### Verification (확인)

"claimant가 그 사람이 맞는가?"

**one-to-one** 비교 -> 사용자 신원이 맞는지 시스템이 해당 사용자가 저장된 정보와 일치하는지만 비교


## Authentication Method

### Knowledge

유저가 아는 정보를 이용해 인증 

Password, PIN 등

### Token

사용자가 소유한 물건을 이용해 인증

OTP 생성기, USB 보안 키, 여권 등

### Biometrics

사용자 신체의 특성이나 행동 패턴을 이용해 인증

- Physiological 특성 - 지문, 홍채, 얼굴 등
- Behavioral 특성 - 서명, 목소리 톤

## Password Based Authentication

### Clear-Text Password

평문 (clear-text)로 데이터베이스에 비밀번호 저장

![[Screenshot 2025-09-15 at 22.33.59.png]]

비밀번호가 데이터베이스에 그대로 노출됨

해커가 데이터베이스를 탈취하면 모든 사용자 아이디와 비밀번호가 즉시 노출

### Message Digests of Passwords

평문 비밀번호를 hash 함수 등으로 변환한 결과값을 이용하여 저장하고 해시 값끼리 비교

이 방법도 **Replay attack (재전송 공격)** 에 취약함


### Replay Attack 해결 방법

#### **nonce** (Number used once)

1. 서버에서 **nonce** 를 생성해서 사용자한테 보냄
2. 사용자는 nonce를 포함해서 비밀번호를 hash
3. 서버는 자신이 보낸 nonce가 맞는지 확인하고 한번 사용된 nonce는 폐기

#### Timestamp

1. 사용자 측에서 요청 보낼 때 현재 시간을 포함하여 보냄
2. 타임스탬프가 현재 서버 시간과의 차이가 짧은지 확인
3. 타임스탬프가 너무 오래전이면 폐기

### Rewrite Attack

암호화된 메시지 내용의 해독(복호화) 없어도 암호화된 메시지를 조작하여 다른 내용으로 바꾸기

- 예시
	- '1000달러 결제'라는 메시지를 `89^&oiu` 로 암호화하여 전송하는데 이걸 가로챔
	- 가로챈 메시지 `89^&oiu`를 `89^&aiu` 로 변경
	- 수신자는 이 메시지를 '9000달러 결제' 라고 해독해버림

### Password-Guessing Attack

비밀번호 추측 공격

#### On-line 공격

로그인 시스템에 아이디와 비밀번호를 계속 입력 (**brute force**)

#### Off-line 공격

서버를 해킹해서 탈취한 **해시된 비밀번호 DB** 를 가지고 자신의 컴퓨터에서 비밀번호를 추측

비밀번호가 저장되는 방식에 의존

#### online 공격 방어 방법

- 로그인 실패 횟수가 증가할수록 다음 시도까지의 대기 시간을 늘리기
- 정해진 횟수 이상 잘못된 비밀번호를 입력하면 계정을 잠그기




### Encrypted Passwords

#### Password encryption for transmission

전송할 때

- 서버와 유저는 **SSL(TLS)** 로 암호화된 커넥션을 먼저 설정
- 모든 정보는 **SSL(TLS)** 를 통해 암호화 됨

#### Password encryption for store

DB에 저장할 때

- 암호화 기법을 통해 읽을 수 없는 형태로 암호화(해싱) 하여 저장

### Protecting Password Files

#### Cryptographic protection

- **One-way Encryption (단방향 암호화)** 알고리즘을 사용하여 저장
- 적절한 암호화 방법 선택해서 **Dictionary attack** 공격을 느리게 만든다.

#### Access control enforced by the OS

- Unix와 Linux는 **shadow password file**에 비밀번호를 저장 (`/etc/shadow`) 
- `/etc/shadow`는 Root 관리자 계정으로만 접근할 수 있음
- 윈도우 NT는 바이너리 형식 파일에 암호화된 비밀번호를 저장 (**Security by Obscurity**)

#### Password Salting

- 비밀번호를 암호화하여 저장할 때, 비밀번호에 임의의 문자열 등을 덧붙이기
- **Dictionary attack**을 지연
- 공격자가 전체 비밀번호 데이터베이스를 한꺼번에 공격하는 대신, 각각의 비밀번호를 따로 공격하도록 강제할 수 있음

## Hashing & Salting

### Hashing

해시된 패스워드를 DB에서 찾음

Dictionary attack에 취약 -> Salting 사용

![[Screenshot 2025-09-16 at 00.56.03.png]]

### Salting

임의의 랜덤값을 추가하여 해시

![[Screenshot 2025-09-16 at 01.13.34.png]]

### Linux Password File

![[Screenshot 2025-09-16 at 01.14.01.png]]

## Authentication Token

사용자가 물리적으로 소유한 작은 장치로 인증

OTP, 2FA 등

-  Token and server are synchronized initially.
	- 두 시스템이 동일한 암호를 생성하기 위한 seed값이 필요
- Token generates fresh passwords periodically.
	- 정해진 시간마다 새로운 비밀번호를 생성
- Same passwords are generated at the server.
	- 서버에서 비밀번호 생성


#### Creation of Token

토큰에 대응되는 **seed** 값을 생성

토큰이 생성될 때마다 인증 서버가 생성

#### Use of Token

- 인증 토큰은 일회용 비밀번호, 패스코드 라고 불리는 **psudorandom** 숫자를 생성한다.
- 서버는 데이터베이스로부터 사용자 ID에 해당하는 **seed**를 얻고, **'Password validation program'** 을 통해서 비밀번호 계산
- 인증 토큰은 비밀번호나 PIN 에 의해 보호


### One-Time Password (OTP)

두 가지 identification 기술이 결합됨

- Knowledge - 일반적인 비밀번호/PIN
- Possession - OTP

#### First approach - 비밀번호 리스트 공유

사용자와 시스템이 **미리 여러 일회용 비밀번호 목록**을 만들어서 양쪽에서 보관

#### Second approach - 순차적 암호 업데이트

사용자와 시스템이 초기 비밀번호 하나를 만들고 그 다음부터 정해진 규칙에 따라 순차적으로 비밀번호를 변경

규칙이 단순하면 다음 비밀번호 예측이 쉽다

#### Third approach - 해시함수 이용

해시함수를 이용하여 비밀번호를 순차적으로 업데이트

![[Screenshot 2025-09-16 at 02.09.30.png]]

공격자가 중간에 비밀번호를 가로채도 해시함수의 단방향성 때문에 이전 비밀번호를 계산할 수 없음

![[Screenshot 2025-09-16 at 02.10.35.png]]

### Challenge-Response

- 요청자는 비밀번호를 알고 있음을 증명
- 비밀번호를 보내지 않고도 그것을 알고 있음을 증명
- **Challenge** 는 **verifier**에 의해 전송되는 시간에 따라 변하는 값

