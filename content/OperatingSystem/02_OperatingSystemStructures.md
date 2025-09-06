---
title: Example Title
description: Example Description
draft: true
tags:
  - example-tag
---
 
The rest of your content lives here. You can use **Markdown** here :)# Operating-system services

## Operating System Services

- User를 위한 services
	- User Interface
	- Program execution
	- I/O operation
	- File-system manipulation
	- Communications
	- Error detection
- Functions for system itself
	- Resource allocation
	- Logging
	- Protection & Security

## Programming Interfaces

### System Call

> 인터럽트를 통해 제공되는 기본적인 프로그래밍 인터페이스
> 어플리케이션 프로그램이 운영체제 커널로부터 서비스를 요청하기 위해 사용되는 메커니즘

`인터럽트를 통해 사용가능한 운영체제 커널에 대한 함수 호출`
보통 interrupt handler로 제공됨

**lower privileged mode에서 higher privileged mode로의 제어권을 안전하게 전달**

#### System-call interface
programming language와 OS간의 연결 (`open()`, `close()`같은 명령어의 구현)

![[Screenshot 2025-04-10 at 22.22.30.png]]

## Dual Mode Operation

### User mode
다른 시스템에 해를 끼칠 수 있는 privileged instruction은 금지됨

🧨`privileged instructions은 오직 OS System Call로만 호출할 수 있다.`

### Kernel mode (supervisor mode, system mode, privileged mode)
privileged instruction 허용

![[Screenshot 2025-04-10 at 22.24.31.png]]

## [[01_Introduction#Interrupt Handling]] 


## Parameter Passing in System Call

내부적으로 시스템 호출은 인터럽트를 통해 서비스되는데 **추가정보가 필요할 수 있음**

### Parameter passing methods
- Register (simple information)
- Address of block (large information)
- System stack

시스템 콜의 종류에 따라 무엇을 사용할지 다르다

![[Screenshot 2025-04-10 at 22.31.50.png]]


## System-Call interface

high level language에서 시스템 호출하는 방법 (ex. `int open(const char *path, int oflag)`)

### System-call interface

> link between runtime support system of programming language and OS system calls

high level language는 OS의 System call (인터럽트)을 직접 노출하지 않고 OS의 기능을 추상화한 함수를 호출 (간접적으로 이용)


![[Screenshot 2025-04-10 at 22.47.37.png]]

겉에서 봤을때는 일반 C언어 함수와 같지만 내부적으로 assembly instruction을 이용해서 인터럽트를 호출한다.

인터럽트 핸들링 메커니즘으로 전환이 되고, 그 순간에 커널 모드로 전환
시스템 콜에 맞는 핸들러를 찾아서 호출

🧨IRQ number와 System call number는 다른 것
![[Screenshot 2025-04-10 at 23.26.44.png]]

1. User program에서 `open()`을 호출
2. System-Call Interface로 가서 assembly로 된 instruction 실행
	1. `movl 5, %eax`는 `eax`레지스터에 `5(open system call number)`를 저장
3. `int $0x80`: 80번 인터럽트를 발생시키는 명령어를 실행 (System Call 전체를 관장하는 하나의 핸들러 실행)
4. Interrupt Handling Mechanism이 실행되는데, system-call handler가 look up하는 **System Call Table**에 있는 어드레스로 function call

인터럽트 핸들러는 같은 번호로 호출되지만 시스템 콜 핸들러는 다르게 호출
(일반적으로 모든 시스템 콜은 하나의 인터럽트만으로 매핑됨, 리눅스틑 0x80, windows는 0x21) 

- 각 System call에는 번호가 연결되어 있다
	- System call interface는 System call number로 인덱싱된 테이블을 유지관리
- System call interface는 OS 커널에서 의돋된 system call을 호출하고, system call의 상태와 return값을 리턴
- System call의 호출자는 시스템이 어떻게 구현되어 있는지 알 필요 없고, 그냥 요청하기만 하면 됨

### System Call Interface가 하는 일

- 커널에 필요한 정보 전달 (파라미터 패싱)
	- 
- 커널 모드로 전환
- 커널모드에서의 실행을 위해 데이터 프로세싱 및 준비

#### System call vs. I/O functions
- `read()`: OS가 제공
- `fread()`: C언어 standard function

`fread()`는 `read()`함수를 사용하여 구현


## Application Programming Interface ( #API )

### API

> OS, 라이브러리, 어플리케이션이 서비스 요청을 허용하기 위해 제공하는 인터페이스

어떤 함수나 메서드를 사용할 수 있는지, 함수에 어떤 파라미터를 전달해야 하는지, 어떤 형태의 리턴 값을 받을 수 있는지 규정

- 프로그래머에게 제공되는 함수, 파라미터, 리턴 값의 집합
- System call과 strongly correlated 관계일 수도 있다.
- System call로 구현된 high-level featrue을 제공할 수 있다.

![[Screenshot 2025-04-11 at 02.11.00.png]]

POSIX의 경우 System Call이 API라고 생각하면 됨
WIN32는 high-level

## Process Control : Load/Execution

프로그램은 다른 프로그램을 load/execute 할 수 있다.

parent program은
- child program으로 대체될 수 있다. (be lost)
- 일시정지될 수 있다.
- 실행을 계속할 수 있다. (multi-programming / multitasking)


### FreeBSD UNIX

![[Screenshot 2025-04-11 at 02.30.43.png]]

`ls`명령어를 실행한 경우

1. Command Interpreter가 ls 명령어를 입력 받음 (쉘은 그냥 프로그램을 실행하는 거임)
2. `fork()`로 자기자신과 똑같은 프로세스를 복사
3. `exec()`으로 child를 실행하고자 하는 프로그램으로 바꿔치기
4. 그동안 parent process (이 경우엔 shell)은 자기 자신 프로세스의 실행을 계속하거나 child process 가 `exit()`할 때까지 대기한다.

- command 인터프리터는 계속 실행가능
- parent process 두가지 경우
	- 계속 실행
		- 새로운 프로그램은 백그라운드에서 실행
	-  자식 프로세스 대기
		- `wait()` 시스템 콜을 통해 자식 프로세스가 종료될 때까지 자신의 실행을 일시정지
		- 새로운 프로세스가 I/O access 가짐

왜 자기랑 똑같은 프로세스 만듬? -> 가장 빠르게 오버헤드가 적게 만드는 방법 (왜 그런지는 가상메모리에서 배움)

쉘에서 명령어 뒤에 `&`를 붙이면 `wait`하지 않고 병렬로 실행



## `fork_demo.c` 예제

`fork_demo.c`
```c
#include <stdio.h>
#include <unistd.h>
int main() {
	fork();
	printf("A\n");
	return 0;
}
```
실행 결과
```bash
A
A
```

`fork()`를 두번 실행
```c
#include <stdio.h>
#include <unistd.h>
int main() {
	fork();
	fork();
	printf("A\n");
	return 0;
}
```
실행 결과
```bash
A
A
A
A
```

child의 `pid_t`값을 받기
```c
#include <stdio.h>
#include <unistd.h>
int main() {
	pid_t child_id = fork();
	printf("cihld_id = %d\n", child_id);

	if(child_id == 0){
		printf("child code\n");
	}else {
		printf("parent code\n");
	}

	return 0;
}
```
실행결과
```bash
child_id = xxxx
parent code
child_id = 0
child code
```

`wait()`사용해보기
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>  // wait() 함수가 정의된 헤더파일
int main() {
	pid_t child_id = fork();
	printf("cihld_id = %d\n", child_id);

	if(child_id == 0){
		printf("child code\n");
	}else {
		wait(NULL) // wait for child process
		printf("parent code\n");
	}

	return 0;
}
```
실행결과
```bash
child_id = xxxx
child_id = 0
child code
parent code
```

🧨 `wait()`은 `<sys/wait.h>` 헤더에 정의되어 있음


## `fork()`, `exec()`, `wait()`

### `fork()`

current 프로세스를 복사하여 자식 프로세스를 생성하는 시스템 콜

### `exec()`

current 프로세스의 메모리 공간을 새로운 프로그램의 코드로 덮어쓰고, 새로운 프로그램 실행

- `l`
	- parameter를 개별 `const char *` 포인터로 전달
	- parameter는 `(char *) NULL` 로 끝나야 한다.
- `p`
	- 실행할 파일 이름에 `/`가 포함돼있지 않으면 `PATH` 환경변수에 지정된 디렉토리들을 검색하여 실행파일을 찾는다.
- `v`
	- parameter를 `char *const argv[]` NULL terminated pointer array로 전달

##### `execlp(const char *file, const char *arg0, ..., const char *argn, (char *)0);`
실행할 파일 이름과 인자들을 리스트 형태로 전달 

##### `execvp(const char *file, char *const argv[])`
실행할 파일 이름과 인자들을 배열 형태로 전달

## Process Control: Load/Execution

- 새로운 프로세스 제어
	- 부모 프로세스는 자식 프로세스의 속성값을 확인하거나 변경가능
	- 프로세스 종료
- 새로운 job, process 대기
	- 고정된 시간동안 wait
	- 이벤트 대기, 이벤트 신호 발생
- 디버깅
	- 덤프 - 메모리 내용 전체 혹은 일부를 파일이나 다른 저장장치치에 기록 (어떤 데이터가 어떤 값이었는지 등을 확인가능)
	- 트레이스 - 모든 명령어 실행 후 트랩

![[Screenshot 2025-04-11 at 15.38.58.png]]

- Termination
	- Normal termination `exit()`
	- Abnormal termination `abort()`
		- 현재 메모리 상태를 파일 하나로 덤프해놓고 죽음

## File Management

- create / delete files
- read / write / reposition
	- **reposition** - 현재 위치를 저장하는 변수를 수정하면 위치 이동 가능
- get / set file attribute
	- 날짜 시간 퍼미션 등
- directory operation
	- 디렉토리를 지우거나 등등

## Device Management

- physical device
	- 디바이스의 인터페이스를 구현한 디바이스 드라이버가 기능을 제공
- abstract/virtual device

#### Combined file-device structure
파일과 장치를 다루는 방식을 통합 -> 파일과 장치에 일관된 인터페이스 제공

즉, 같은 `read()`, `write()`, `open()`, `close()`등의 시스템콜을 동일하게 사용

## Information Maintenance

- OS와 유저 프로그램 사이에 정보 전달
	- ex) current time, date

`OS는 모든 프로세스에 대한 정보를 유지 관리한다`
Linux의 `/proc` 디렉토리의 정보들은 커널 내부의 변수들인데 이것을 파일인 것처럼 가상 파일로 보여주는 것

## System Program

> 환경을 제공해주기 위한 application program

"커널은 환경을 제공하는 것이다"
커널 말고도 프로그램에서 제공하는 환경도 있다. (ex 쉘)


# Components and their interconnections

## Simple Structure

MS-DOS 같은 경우에는 싱글 유저 시스템으로 한번에 하나의 프로그램만 실행할 수 있었음
application 프로그램이 ROM-BIOS도 실행할 수 있었고, 하드웨어까지 다룰 수 있었음.

## Monolithic Structure

운영체제 핵심기능을 하나의 커널 공간에 통합
- 하나 고장나면 다 고장남
- 유지보수, 확장이 힘들다

![[Screenshot 2025-04-11 at 16.26.22.png]]

리눅스는 모놀리식 구조지만 커널이 모듈화 되어있다.

모놀리식 기능간의 통신이 효율적이다 (서로가 서로를 호출가능)

## Layered Approach
한 덩어리라서 관리하기 어려운 monolithic structure의 단점을 극복하기 위한 아이디어

- layer 0 - hardware
- layer 1 - 가장 기본적인 primitives
- layer 2 - 하드웨어와 layer 1을 사용해서 작성
- layer n - 내부의 코드를 바깥에서 호출

디버깅과 개발이 쉽다 (자기보다 상위 레이어는 사용하지 않으며, 하위 레이어는 이미 디버깅과 개발이 끝났기 때문에 신경쓸 일이 적다)

#### 예시 - 메모리 매니저

![[Screenshot 2025-04-11 at 16.34.23.png]]

**Backing store driver**- 가상 메모리 구현을 위한 모델

Layered Approach를 사용할 때는 관계 설계를 잘 해야한다.

## Microkernel

정말 커널에서 필요한 기능만 구현하고 나머지는 user level program으로 분리 

- 커널을 최소화 함으로써 시스템 충돌 시 위험성을 줄인다 (안정성)
- 확장성
- 멀티 프로세싱 환경/ 클러스터드 시스템에서는 남의 컴퓨터에 있는 API를 호출할 수 있다. (병렬 컴퓨팅에 도움)

### Message Passing
마이크로커널에서 시스템 콜은 **message passing**을 통해 제공
일종의 interprocess communication

단점으로 속도가 느려짐 (메시지 패싱을 거치기 때문에)

커널에 들어가는 기능
- 프로세스 스케줄링
- 메모리 관리
- 인터프로세스 커뮤니케이션 (메시지 패싱을 위해 필수)


## Loadable Kernel module (LKM)

- 객체지향 접근법
- 각 core 컴포넌트는 분리돼있음
- 서로 인터페이스를 통해 통신
- 필요에 따라 커널에 로드 가능

커널의 핵심기능을 가운데 넣고 나머지 파트를 모듈형태로 탈착 가능하게 구성

#### Microkernel과 차이점
> Microkernel은 핵심 커널 기능 외의 기능은 user mode에서 동작하지만,
> LKM의 모듈은 커널 모드에서 동작한다.

- Layered Structure에 비해 
	- 유연하다
- Microkernel에 비해
	- 각 모듈을 커널모드에서 실행할 수 있다.
	- 퍼포먼스가 좋다 (메시지 패싱 안해서))

![[Screenshot 2025-04-11 at 18.50.50.png]]

## Hybrid System

실제로는 위에서 다룬 여러 OS 구조를 섞어서 사용함

- **Linux, Solaris**: monolithic, modular for dynamic loading of functionality
- **Windows**: monolithic, microkernel
- **Mac OS X**:  hybrid, layered
### MacOS, iOS
![[Screenshot 2025-04-12 at 13.38.01.png]]

- Kernel environment (**Darwin**): Hybrid Structure
![[Screenshot 2025-04-12 at 13.38.44.png]]

