---
title: 소켓 프로그래밍 - 버클리 소켓
description:
draft: false
tags:
  - computer_network
  - network_programming
  - cpp
---
# 버클리 소켓 API

## 1. 소켓 만들고 닫기

```cpp
// Windows
#include <WinSock2.h>
SOCKET socket(int af, int type, int protocol);

// Linux
#include <sys/socket.h>
#include <sys/types.h>
int socket(int domain, int type, int protocol);
```

첫번째 파라미터는 **Address Family** 를 의미한다. 보통 `AF_INET` (IPv4) 를 사용한다.

| 매크로         | 의미      |
| ----------- | ------- |
| `AF_INET`   | IPv4    |
| `AF_INET6`  | IPv6    |
| `AF_UNSPEC` | 지정하지 않음 |

소켓으로 주고받을 패킷의 종류를 `type` 파라미터로 지정한다.


| 매크로              | 의미                                             |
| ---------------- | ---------------------------------------------- |
| `SOCK_STREAM`    | 순서와 전달이 보장되는 데이터 스트림<br>스트림의 각 세그먼트를 패킷으로 주고받음 |
| `SOCK_DGRAM`     | 각 데이터그램을 패킷으로 주고받음                             |
| `SOCK_RAW`       | 패킷 헤더를 Application Layer에서 직접 만들 수 있음          |
| `SOCK_SEQPACKET` | `SOCK_STREAM`과 유사하지만 패킷 수신 시 항상 전체를 읽음         |
`SOCK_STREAM` 은 연결지향형 (TCP), `SOCK_DGRAM` 은 비 연결지향형 (UDP) 라고 생각하면 편할듯 하다.

<br>

`protocol` 파라미터는 소켓이 데이터 전송에 사용하는 프로토콜의 종류를 명시한다.


| 매크로                 | 필요 소켓 종류      | 의미                          |
| ------------------- | ------------- | --------------------------- |
| `IPPROTO_UDP`       | `SOCK_DGRAM`  | UDP 데이터그램 패킷                |
| `IPPROTO_TCP`       | `SOCK_STREAM` | TCP 세그먼트 패킷                 |
| `IPPROTO_IP` or `0` | \*            | `type` 파라미터에 따라 디폴트 프로토콜 사용 |
보통 `0` 으로 설정하여 OS가 알아서 소켓 type에 맞는 프로토콜을 선택하도록 하면 된다.

<br>
소켓을 닫으려면

```cpp
// Windows
#include <winsock2.h>
int closesocket(SOCKET sock);

// Linux
#include <unistd.h>
int close(int fd); // 리눅스에서는 소켓 디스크립터를 파일 디스크립터와 동일하게 처리
```

`close`와 `closesocket` 함수호출은 **완전 종료**를 의미한다. TCP의 경우 Full-Duplex 통신이므로 양방향으로 보내고 받는 연결 통로가 존재한다. `close`나 `closesocket`으로 소켓을 닫으면 송수신을 모두 차단하게 된다. 

만약 클라이언트가 서버에 데이터를 다 보낸 뒤에 `close` 했는데 서버가 아직 ACK 을 보내는 중이었다면 그 응답을 받지 못하고 연결이 강제로 끊기는 문제가 있다.
서버 입장에서는 데이터를 더 보낼 의사가 없는 것인지, 프로그램이 죽은 건지 구분할 수 없다.

TCP 소켓을 우아하게 닫으려면 `shutdown()` 함수를 사용한다.

```cpp
// windows
int shutdown(SOCKET sock, int how);

//Linux
int shutdown(int s, int how);
```


| 매크로 (리눅스 매크로)            | 의미                    |
| ------------------------ | --------------------- |
| `SD_SEND` (`SHUT_WR`)    | 전송 중단 (**FIN** 패킷 전송) |
| `SD_RECEIVE` (`SHUT_RD`) | 수신 중단                 |
| `SD_BOTH` (`SHUT_RDWR`)  | 송수신 모두 중단             |

한쪽이 FIN 패킷을 보내면 상대방도 FIN 패킷을 응답하게 되고 소켓을 Graceful 하게 닫을 수 있다.

소켓을 닫으면 리소스를 OS에 반납한다. 사용을 마친 소켓은 반드시 닫아야 한다.

<br>

---
<br>

## 2. 운영체제별 API 차이

### 헤더 파일 차이

#### Windows (WinSock)

```cpp
#define WIN32_LEAN_AND_MEAN  
#include <winsock2.h>  
#include <ws2tcpip.h>  
#include <windows.h>             // close()
```

`Windows.h` 를 include 하기 전에 `WinSock2.h` 를 먼저 include 하거나,
`Windows.h` 를 include 하기 전에 `WIN32_LEAN_AND_MEAN` 매크로를 `#define` 해야 한다.

추가적으로 라이브러리 링크가 필요하다.
Visual Studio의 경우에는 `Ws2_32.lib`, gcc (MinGW) 의 경우에는 `-lws2_32`
#### Linux (Posix 표준)
```cpp
#include <unistd.h>             // close()
#include <arpa/inet.h>          // inet_pton, htons
#include <sys/socket.h>         // socket, bind, listen
#include <netinet/in.h>         // sockaddr_in
```

### 초기화 차이

리눅스는 기본적으로 초기화가 전혀 필요 없다
윈도우에서는 명시적으로 초기화와 마무리를 해야 한다.

초기화에는 `WSAStartup()` , 마무리는 `WSACleanup()` 을 호출한다.

```cpp
int WSAStartup(WORD wVersionRequested, LPWSADATA lpWSAData);
```

`wVersionRequest` 는 2바이트 워드로 하위 바이트는 주버전, 상위 바이트는 부 버전이다.
현시점 최신 버전은 2.2 이므로 `MAKEWORD(2,2)` 를 인자 값으로 넘기면 된다.

`lpWSAData` 는 윈도우 전용 구조체인데, 활성화된 라이브러리에 대한 정보로 값을 채워준다. 잘 쓰이지는 않는다.

`WSAStartup()` 성공 시 0, 실패 시 에러 코드를 리턴한다.

```cpp
WSADATA wsa;
WSAStartup(MAKEWORD(2,2), &wsa);
```

<br>

```cpp
int WSACleanup();
```

`WSACleanup()` 의 리턴값은 에러 코드이다. 

호출 시 모든 소켓 동작이 강제 종료되고 소켓 리소스가 소멸된다.

`WSAStartup()` 은 레퍼런스 카운트되기 때문에 `WSAStartup()` 호출 횟수만큼 `WSACleanup()`을 호출해줘야 한다.

### 에러 처리 차이

리눅스가 `errno.h` 의 `errno` 전역 변수를 사용하는 것과 다르게
윈도우에서는 `WSAGetLastError()` 함수를 사용한다.

```cpp
// Windows
if (sock == INVALID_SOCKET) {
	printf("error: %d\n", WSAGetLastError());
}

// Linux
if (sock == -1) {
	perror("socket error"); // 에러값 - errno
}
```

`WSAGetLastError()` 함수는 실행중인 스레드에서 마지막으로 발생한 에러코드만 저장하기 때문에 소켓 라이브러리 함수 리턴값으로 `-1`을 받으면 즉시 확인할 수 있도록 한다.

`errno`도 다른 소켓이나 C 표준 함수를 호출할 때 덮어 쓰일 수 있기 때문에 에러 감지 시점에 확인해야 한다.

<br>

---

<br>

## 3. 소켓 주소

소켓은 어플리케이션과 네트워크 프로토콜 사이의 인터페이스이다. Transport layer 의 패킷은 IP 주소와 더불어 포트 번호가 필요하다.

```cpp
struct sockaddr {
	uint16_t sa_family;  // 주소 체계 (ex: AF_INET)
	char sa_data[14];    //  주소 정보 (IP + Port)
};
```

모든 소켓 API 함수는 공통적으로 `sockaddr` 포인터를 인자로 받는데, 실제 프로그래밍에서 바이트 배열로 된 `sa_data` 에 값을 일일이 넣기 불편하다. IPv4 패킷용 주소를 만들기 위해 `sockaddr_in` 을 사용할 수 있다.

```cpp
struct sockaddr_in {
	short sin_family;
	uint16_t sin_family;
	struct in_addr sin_addr; // 4 bytes IPv4 주소
	char sin_zero[8]; // 사용하지 않는 크기 맞추기용 패딩 값. 0으로 채우면 됨
};
```

`sockaddr_in` 은 **"IPv4"** 패킷용 주소를 만들기 위해 사용하므로 `sin_family`는 없어도 될 것 같지만 타입 캐스팅 시 `sockaddr`과 동일한 바이트 열을 가져가야 하므로 어쩔 수 없다.
`sockaddr`는 IPv4 말고 다른 family의 주소 정보도 담을 수 있는 구조체다.

`in_addr`의 내부 정의 방식은 윈도우와 리눅스가 다르다.

```cpp
// Windows
struct in_addr {
	union {
		struct { uint8_t s_b1, s_b2, s_b3, s_b4; } S_un_b;
		struct { uint16_t s_w1, s_w2; } S_un_w;
		uint32_t S_addr;
	} S_un;
};

// Linux
struct in_addr {
	in_addr_t s_addr; // typedef uint32_t in_addr_t;
};
```

리눅스가 `in_addr_t` (`uint32_t`) 정수 하나인데 반해,
윈도우는 유니온 구조로 바이트/워드 단위로 접근 가능하도록 했다. (이게 더 좋은듯)

<br>

#### 네트워크 바이트 순서 (Byte Order) 와 인터넷 주소 변환

IP 주소와 포트 번호를 설정할 때 바이트 배열로 묶어서 사용하려고 할 때  CPU마다 메모리에 저장하는 순서가 다르다.

상위 바이트의 값을 작은 번지수에 저장하는 방식을 **빅 엔디안 (Big Endian)**,
상위 바이트의 값을 큰 번지수에 저장하는 방식을 **리틀 엔디안 (Little Endian)** 이라고 한다.



4바이트 정수 1 (`0x00000001`) 을 메모리에 저장하려고 할 때 빅 엔디안과 리틀 엔디안의 차이는 아래와 같다.

| 엔디안    | 저장 순서      | 메모리 모습 (낮은 주소 -> 높은 주소) | 사용처                 |
| ------ | ---------- | ----------------------- | ------------------- |
| 빅 엔디안  | 높은 자릿수가 앞에 | `00` `00` `00` `01`     | TCP/IP 네트워크 표준      |
| 리틀 엔디안 | 낮은 자릿수가 앞에 | `01` `00` `00` `00`     | Intel/AMD (Windows) |

**"빅 엔디안은 사람이 숫자를 읽는 방식과 똑같다"** 라고 이해하면 편하다.

헷갈리지 말아야 할 점은 "바이트 순서" 가 다르다는 점이다.

`0x12345678` 을 리틀 엔디안으로 표현할 때 `0x87654321` 이라고 생각하면 오산이다.
`0x78563412`가 맞는 표현임을 절대 잊지말기.

위처럼 플랫폼마다 바이트 순서가 다를 수 있기 때문에 소켓 주소 구조체를 정의할 때 호스트의 순서가 아닌 네트워크가 이해하는 순서로 변환해야 한다.

`htons()`와 `htonl()` 을 사용하여 네트워크 바이트 순서로 변환할 수 있다.


```cpp
uint16_t htons(uint16_t hostshort);
uint32_t htonl(uint32_t hostlong);
```

각각 16비트, 32비트 정수에 대해 호스트의 네이티브 바이트 순서에서 네트워크 바이트 순서로 변환한다.

호스트와 네트워크의 바이트 순서가 같은 경우 컴파일러 최적화 시 함수 호출해도 아무 동작도 안한다.

네트워크 바이트 순서를 다시 호스트 바이트 순서로 변환하려면 `ntohs()`와 `ntohl()`을 사용하면 된다.

```cpp
uint16_t ntohs(uint16_t networkshort);
uint32_t ntohl(uint32_t networklong);
```

데이터 송수신 시에는 네트워크 바이트 순서로 변환할 필요 없이 자동으로 된다. (휴)


앞서 배운 코드들을 통해 `sockaddr_in` 구조체를 초기화 하는 과정이다.

```cpp
sockaddr_in myAddr;
memset(myAddr.sin_zero, 0, sizeof(myAddr.sin_zero));
myAddr.sin_family = AF_INET;
myAddr.sin_port = htons(80);
myAddr.sin_addr.S_un.S_un_b.s_b1 = 127;
myAddr.sin_addr.S_un.S_un_b.s_b2 = 0;
myAddr.sin_addr.S_un.S_un_b.s_b3 = 0;
myAddr.sin_addr.S_un.S_un_b.s_b4 = 1;
```

### 자료형 안정성 (Type Safety)

소켓 기본 데이터 타입과 함수를 객체 지향 형태로 래핑해서 타입 안정성과 추상화를 챙길 수 있다.

```cpp
class SocketAddress
{
public:
	SocketAddress(uint32_t inAddress, uint16_t inPort) {
		GetAsSockAddrIn()->sin_family = AF_INET;
		GetAsSockAddrIn()->sin_addr.S_un.S_addr = htonl(inAddress);
		GetAsSockAddrIn()->sin_port = htons(inPort);
	}

	SocketAddress(const sockaddr& inSockAddr) {
		memcpy(&mSockAddr, &inSockAddr, sizeof(sockaddr));
	}

	size_t GetSize() const {
		return sizeof(sockaddr);
	}

private:
	sockaddr mSockAddr;

	sockaddr_in* GetAsSockAddrIn() {
		// (sockaddr_in*)(&mSockAddr); // C 스타일 casting
		return reinterpret_cast<sockaddr_in*>(&mSockAddr);
	}
};

// typedef std::shared_ptr<SocketAddress> SocketAddressPtr; // C 스타일
using SocketAddressPtr = std::shared_ptr<SocketAddress>;
```

C 소켓 API는 `sockaddr` 이라는 공통된 구조체로 주소 정보를 다루지만, 실제로 데이터를 채워넣는 과정에서는 `sockaddr_in`, `sockaddr_in6` (IPv6 용) 으로 강제 형변환을 해야 한다.

`SockAddress` 클래스를 만들어 `GetAsSockAddrIn()` 함수를 통해 내부에서 형변환을 처리하면, 외부에서는 `sockaddr_in`의 메모리 구조를 몰라도 생성자만으로 `mSockAddr`의 내용물을 채울 수 있다.

마지막 `SocketAddressPtr`을 Type Alias로 소켓 주소 공유해서 쓰고 메모리 정리 자동으로 되기 한다.

### 문자열로 `sockaddr` 초기화하기

`sockaddr`에 IP 주소와 포트 번호를 하나씩 채워넣기 번거로운데, `inet_pton()`, `InetPton()` 함수로 IP주소 문자열을 이진 IP 주소로 변환할 수 있다.

```cpp
// Windows
int InetPton(int af, const PCTSTR src, void* dst);

// Linux
int inet_pton(int af, const char* src, void* dst);
```

주소 family `af`는 `AF_INET`이나 `AF_INET6` 를 넘기면 되고,

`src`는 문자열 IP 주소를 넘기면 된다.

`dst` 에는 변환된 `sin_addr` 주소 필드의 포인터를 넘기면 된다.

```cpp
sockaddr_in myAddr;
myAddr.sin_family = AF_INET;
myAddr.sin_port = htons(80);
InetPton(AF_INET, "127.0.0.1", &myAddr.sin_addr);
```

성공 시 `1`, 문자열 해석 불가면 `0`, 시스템 에러는 `-1` 리턴한다.


도메인 이름으로 IP 주소를 알고 싶으면 `getaddrinfo()` 함수를 사용한다.

```cpp
int getaddrinfo(const char* hostname,
				const char* servname,
				const addrinfo* hints,
				addrinfo** res
);
```

- `hostname`: 도메인 조회를 할 이름 문자열
- `servname`: 포트 번호 또는 서비스 이름 (ex: `"80"`, `"http"`)
- `hints`: 어떤 정보를 받고 싶은지를 기재한 `addrinfo` 구조체의 포인터를 넘긴다.
- `res`: 도메인 조회 결과가 여러 개일 수 있기 때문에 Linked List 형태로 반환되는데, `res`가 첫번째 요소가 된다.

`addrinfo` 구조체의 내용물은 다음과 같다.

```cpp
struct addrinfo {
	int ai_flags;
	int ai_family;
	int ai_socktype;
	int ai_protocol;
	size_t ai_addrlen;
	char* ai_canon_name;
	sockaddr* ai_addr;
	addrinfo* ai_next;
};
```

- `ai_flags`, `ai_socktype`, `ai_protocol`는  `hints` 요구사항 정의에 사용한다.
- `ai_canon_name`: 리졸브된 호스트명의 **CNAME (canonical name)**을 담는다.
- `ai_addr`: `getaddrinfo()` 호출 시 지정한 호스트와 포트 조합이 가리키는 주소 정보
- `ai_next`: linked list 상 다음 `addrinfo` 포인터

`getaddrinfo()`가 `addrinfo` 구조체 반환할 때 자체적으로 메모리를 할당하는데, `freeaddrinfo()` 함수로 메모리를 해제해줘야 한다.

```cpp
void freeaddrinfo(addrinfo* ai);
```

- `ai`: 반드시 `getaddrinfo()` 로 받은 첫 번째 `addrinfo` 를 넘겨줘야 함


`getaddrinfo()` 가 DNS 패킷을 만들어 응답을 기다리고, linked list를 만들어 리턴할 때까지 시간이 많이 걸릴 수 있다. `getaddrinfo()`는 비동기 동작을 지원하지 않기 때문에 호출한 스레드에서는 블로킹돼있어야 한다.

윈도우에서는 `GetAddrInfoEx()` 를 사용해서 비동기식으로 동작하게 하는 옵션을 제공할 수 있다.

`SocketAddressFactory`로 도메인 네임 resolution 하는 코드는 아래와 같다.

```cpp
class SocketAddressFactory
{
public:
	static SocketAddressPtr CreateIPv4FromString(const std::string& inString) {
		// 콜론 기준으로 host와 port 분리
		auto pos = inString.find_last_of(':');
		std::string host, service;
		if ( pos != std::string::npos ) { // string::npos - 찾는 문자열이나 문자가 있다면 host와 service(port) 분리
			host = inString.substr(0, pos);
			service = inString.substr(pos + 1);
		}
		else { // 포트가 지정되지 않았으므로 디폴트 사용
			host = inString;
			service = "0";
		}

		// getaddrinfo 에 IPv4 주소만 찾도록 hint 설정
		addrinfo hint;
		memset(&hint, 0, sizeof(hint));
		hint.ai_family = AF_INET;

		addrinfo* result = nullptr;
		int error = getaddrinfo(host.c_str(), service.c_str(), &hint, &result);
		addrinfo* initResult = result;

		if ( error != 0 && result != nullptr ) {
			freeaddrinfo(initResult);
			return nullptr;
		}
		
		// linked list 돌면서 실제 주소 데이터 (ai_addr)이 있는 첫번째 노드를 찾기
		while(!result->ai_addr && result->ai_next ){
			result = result->ai_next;
		}

		if ( !result->ai_addr ) {
			freeaddrinfo(initResult);
			return nullptr;
		}

		// ai_addr 있는 노드를 찾았으면 SocketAddress 객체를 shared 로 생성 
		auto toRet = std::make_shared<SocketAddress>(*result->ai_addr);

		freeaddrinfo(initResult);
		return toRet;
	}
};
```


### 소켓 바인딩하기

운영체제에 소켓이 특정 주소와 transport layer 포트를 사용하겠다고 알리는 것을 바인딩이라고 한다.
`bind()` 함수로 IP 주소와 포트를 바인딩할 수 있다.

```cpp
// Windows
int bind(SOCKET sock, const sockaddr* address, int address_len);

// Linux
int bind(int sock, const struct sockaddr *address, socklen_t addrlen);
```

`address`에 바인딩할 소켓 주소가 들어간다. 패킷을 보내는 주소가 아니라 패킷을 받을 때 사용하는 자신의 주소를 정의한다. 한 컴퓨터에 IP가 여러 개 존재하는 경우가 있기 때문에 필요하다.

게임 서버 관점에서 보면 모든 네트워크 인터페이스와 IP 주소에 대해 포트를 바인딩하고 싶은 경우가 더 많다. 
바인딩 할 주소로 `sockaddr_in`의 `sin_addr` 필드에 `INADDR_ANY` (IPv4 0.0.0.0) 을 넣어주면 된다.

바인딩이 되면 OS가 바인딩한 주소와 포트를 목적지로 발신된 패킷을 이 소켓으로 넘겨준다. (Demultiplexing)

보통 주소와 포트 쌍 하나에 하나의 소켓을 바인딩할 수 있는데, 같은 조합에 중복으로 바인딩 시도 시 에러난다.
아직 사용중이지 않은 포트에 바인딩을 하려면 `bind()` 호출 시 포트를 0으로 설정하면 된다.

## UDP 소켓

UDP 소켓은 만들고 바로 데이터를 보낼 수 있다. `sendto()` 함수를 사용한다.

```cpp
// Windows
int sendto(SOCKET sock, const char* buf, int len, int flags,
			const sockaddr* to, int tolen
);

// Linux
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
				const struct sockaddr *dest_addr, socklen_t addrlen
);
```

- `sock`: 데이터그램을 보낼 소켓. 바인딩 돼있지 않은 경우 자동으로 바인딩 해준다.
- `buf`: 보낼 데이터의 시작 주소
- `len`: 데이터 길이. MTU 사이즈 때문에 packet fragmentation없이 보내려면 1300바이트 이내로
- `flags`: 데이터 전송 제어 비트 플래그. 보통 `0`
- `to`: 목적지 `sockaddr`
- `tolen`: `sockaddr`길이. IPv4에서는 `sizeof(sockaddr_in)` 사용

성공 시 데이터의 길이, 실패시 `-1` 리턴

UDP 소켓으로 데이터를 받으려면 `recvfrom()` 함수를 사용한다.

```cpp
// Windows
int recvfrom(SOCKET sock, char *buf, int len, int flags,
				struct sockaddr *from, int* fromlen
);

// Linux
ssize_t recvfrom(int sockfd, char *buf, int len, int flags,
				struct sockaddr *src_addr, socklen_t *addrlen 
);
```

- `flags`: `MSG_PEEK`이 가끔 쓰이는데, 수신된 데이터그램을 `buf`로 복사하지만 Input Queue에서는 제거하지 않기 때문에 수신된 데이터의 크기를 미리 확인하거나 내용을 확인 하고, 현재 버퍼 크기가 부족하면 다음에 동일한 데이터를 받을 때 더 큰 버퍼를 미리 준비하고 가져올 수 있다.
- `from`: 데이터를 받았을 때, 발신자의 주소와 포트로 채워진다.

UDP는 TCP와 다르게 연결지향형이 아니므로, 여러 발신자가 하나의 주소와 포트 소켓에 패킷을 보낼 수 있다. 각 데이터그램이 어디서 왔는지 확인하는 용도로 필요하다.


<br>


### 자료형 안전성을 보강한 UDP 소켓 클래스

```cpp
class UDPSocket
{
public:
  ~UDPSocket();
  int Bind(const SocketAddress& inBindAddress);
  int SendTo(const void* inData, int inLen, const SocketAddress& inToAddress);
  int RecvFrom(void* inBuffer, int inLen, SocketAddress& outFromAddress);

private:
  friend class SocketUtil;
  UDPSocket(SOCKET inSocket) : mSocket(inSocket) {}
  SOCKET mSocket;
};

typedef shared_ptr<UDPSocket> UDPSocketPtr;

int UDPSocket::Bind(const SocketAddress& inBindAddress) {
  int err = bind(mSocket, &inBindAddress.mSockAddr, inBindAddress.GetSize());

  if (err == 0)
    return 0;

  SocketUtil::ReportError("UDPSocket::Bind");
  return SocketUtil::GetLastError();
}

int UDPSocket::SendTo(const void* inData, int inLen, const SocketAddress& inToAddress) {
  int byteSendCount = sendto(
    mSocket,
    inData,
    inLen,
    0,
    &inToAddress.mSockAddr,
    inToAddress.GetSize()
  );

  if (byteSendCount >= 0)
    return byteSendCount;


  // 에러 코드를 음수로 리턴
  SocketUtil::ReportError("UDPSocket::SendTo");
  return -SocketUtil::GetLastError();
}

int UDPSocket::RecvFrom(void* inBuffer, int inLen, SocketAddress& outFromAddress) {

  socklen_t fromLength = outFromAddress.GetSize();

  int readByteCount = recvfrom(
    mSocket,
    inBuffer,
    inLen,
    0,
    &outFromAddress.mSockAddr,
    &fromLength
  );

  if (readByteCount >= 0)
    return readByteCount;

  SocketUtil::ReportError("UDPSocket::RecvFrom");
  return -SocketUtil::GetLastError();
}


UDPSocket::~UDPSocket() {
  close(mSocket);
}
```


`SocketAddress` 에서 `UDPSocket`을 `friend` 클래스로 선어해서 `sockaddr` private 멤버변수를 직접 수정할 수 있다.

`~UDPSocket()` 소멸자로 소켓을 자동으로 닫아줄 수 있도록 한다.

`SocketUtil` 클래스를 따로 두어 `UPDSocket` 에서 발생한 오류를 보고하도록 한다. 플랫폼마다 다르게 처리하기 편해진다.

직접 `UDPSocket`을 만들 수 있는 함수가 존재하지 않는데, `UDPSocket` 객체가 있다면 그 `mSocket`은 무조건 열려있음을 보장할 수 있다.
`SocketUtil` 클래스를 활용해서 소켓 생성을 맡기도록 한다.

```cpp
// SocketUtil.cpp
enum SocketAddressFamily {
  INET = AF_INET,
  INET6 = AF_INET6
};

int SocketUtil::GetLastError() {
  return errno;
}

void SocketUtil::ReportError(const char* inOperationDesc) {
  Log::Error(inOperationDesc);
}

UDPSocketPtr SocketUtil::CreateUDPSocket(SocketAddressFamily inFamily) {
  SOCKET s = socket(inFamily, SOCK_DGRAM, IPPROTO_UDP);
  if (s != -1)
    return UDPSocketPtr(new UDPSocket(s));

  ReportError("SocketUtil::CreateUDPSocket");
  return nullptr;
}
```

## TCP 소켓

UDP는 연결을 유지하지 않으며 신뢰성을 보장하지 않는다. 따라서 하나의 소켓으로 여러 호스트에서 오는 데이터그램을 받을 수 있다.
TCP는 TCP 연결마다 별개의 소켓을 유지해야 한다.

초기 연결에는 3-way handshaking이 필요하다. `socket()`으로 소켓을 만들고 `bind()` 이후, `listen()`을 통해 소켓으로 들어오는 핸드셰이킹을 리스닝한다.

```cpp
// Windows
int listen(SOCKET sock, int backlog);

// Linux
int listen(int sock, int backlog);

// 성공 시 0, 에러 시 -1
```

- `backlog`: 연결 요청을 대기시킬 큐의 크기이다.
	- 윈도우에서는 `SOMAXCONN` (허용 가능한 최대치) 을 기본값으로 한다.

리스닝 소켓은 다른 호스트와 연결되는 게 아니라, 새로 들어오는 연결 요청을 받아 새로운 소켓을 만들어주는 역할만 수행한다.

연결 요청을 승인해서 TCP 핸드셰이킹 과정을 진행하려면 `accept()`를 사용한다.

```cpp
// Windows
SOCKET accept(SOCKET sock, sockaddr* addr, int* addrlen);

// Linux
int accept(int sock, sockaddr* addr, socklen_t* addrlen);

// 성공 시 통신하는 소켓, 에러 시 -1
```

- `addr`: 연결을 요청하는 호스트의 주소를 채울 `sockaddr` 구조체 포인터
- `addrlen`: `addr`의 길이

`accept()`가 받아줄 연결 요청이 없는 상태이면 기본적으로 블로킹 상태로 대기한다.

클라이언트 입장에서는 연결 요청을 `listen()` 하고, `accept()` 로 수락할 필요 없이 자기 자신이 서버와의 통신에 사용할 소켓을 만들고 `connect()`만 호출하면 된다.

```cpp
// Windows
int connect(SOCKET sock, const sockaddr* addr, int addrlen);

// Linux
int connect(int sock, const sockaddr* addr, socklen_t addrlen);

// 성공 시 0, 에러 시 -1
```

- `addr`: 연결하고자 하는 호스트의 주소
- `addrlen`: `addr`의 길이

`connet()` 호출 시 SYN 패킷을 전송해서 3-way handshaking을 시작한다.

<br>

연결된 TCP 소켓은 remote 호스트의 주소 정보를 가지고 있기 때문에, UDP 처럼 데이터 송수신마다 주소 정보를 넘겨줄 필요가 없다. `sendto()`와 `recvfrom()`대신 `send()`와 `recv()` 함수를 사용한다.

`send()` 함수 시그니처는 아래와 같다.

```cpp
// Windows
int send(SOCKET sock, const char* buf, int len, int flags);

// Linux
ssize_t send(int sock, const void *buf, size_t len, int flags);

// 성공시 데이터 사이즈 리턴, 에러 시 -1 (SOCKET_ERROR) 리턴
```

UDP와는 다르게 MTU보다 작게 `len`을 잡을 필요 없다.

`flags` 는 데이터 전송을 제어하는 비트 플래그이다. 보통 `0`으로 한다.

`send()` 성공 시 전송한 데이터의 사이즈를 리턴하는데, `len`에 명시한 값보다 작으면, 소켓의 전송 버퍼가 `len`만큼 보내기에 충분하지 않아서 여유 공간만큼만 보냈다는 의미이다.

TCP는 기본적으로 메시지 경계가 없다는 것에 주의하고, `send()`로 보내려고 의도한 데이터가 무조건 전송 완료될 거라고 기대해서는 안된다.

```cpp
// Windows
int recv(SOCKET sock, const char* buf, int len, int flags);

// Linux
ssize_t recv(int sock, void* buf, size_t len, int flags);

// 성공 시 수신한 데이터 사이즈 리턴, 에러 시 -1 리턴
```

`recv()` 성공 시 수신한 데이터의 사이즈를 리턴하는데, `len`에 명시한 값보다 작거나 같다. 상대편이 `send()`를 보냈을 때 `recv()`로 같은 길이의 데이터를 받는다고 보장할 수 없다.

`len`에 0을 넣어서 `recv`를 호출했을 때 리턴값이 `0`이면 소켓에 읽을 것이 남아 있다는 뜻이다. (표준 동작은 아니긴 함) 

### 자료형 안전성을 보강한 TCP 소켓 클래스

```cpp
// TCPSocket.h , TCPSocket.cpp
class TCPSocket;
using TCPSocketPtr = shared_ptr<TCPSocket>;

class TCPSocket {

public:
  ~TCPSocket();
  int Connect(const SocketAddress& inAddress);
  int Bind(const SocketAddress& inToAddress);
  int Listen(int inBackLog = 32);
  TCPSocketPtr Accept(SocketAddress& inFromAddress);
  int Send(const void* inData, int inLen);
  int Recv(void* inBuffer, int inLen);

private:
  friend class SocketUtil;
  TCPSocket(SOCKET inSocket) : mSocket(inSocket) {}
  SOCKET mSocket;
};

int TCPSocket::Bind(const SocketAddress& inBindAddress) {
  int err = bind(mSocket, &inBindAddress.mSockAddr, inBindAddress.GetSize());

  if (err == 0)
    return 0;

  SocketUtil::ReportError("UDPSocket::Bind");
  return SocketUtil::GetLastError();
}

int TCPSocket::Connect(const SocketAddress& inAddress) {
  int err = connect(mSocket, &inAddress.mSockAddr, inAddress.GetSize());
  if (err >= 0)
    return 0; // NO_ERROR;

  SocketUtil::ReportError("TCPSocket::Connect");
  return -SocketUtil::GetLastError();
}

int TCPSocket::Listen(int inBackLog) {
  int err = listen(mSocket, inBackLog);
  if (err >= 0)
    return 0;

  SocketUtil::ReportError("TCPSocket::Listen");
  return -SocketUtil::GetLastError();
}

TCPSocketPtr TCPSocket::Accept(SocketAddress& inFromAddress) {
  socklen_t length = inFromAddress.GetSize();
  SOCKET newSocket = accept(mSocket, &inFromAddress.mSockAddr, &length);

  if (newSocket != -1) // newSocket != INVALID_SOCKET
    return TCPSocketPtr(new TCPSocket(newSocket));

  SocketUtil::ReportError("TCPSocket::Accept");
  return nullptr;
}

int TCPSocket::Send(const void* inData, int inLen) {
  int bytesSentCount = send(
    mSocket,
    static_cast<const void*>(inData),
    inLen,
    0
  );

  if (bytesSentCount >= 0)
    return bytesSentCount;

  SocketUtil::ReportError("TCPSocket::Send");
  return -SocketUtil::GetLastError();
}

int TCPSocket::Recv(void* inBuffer, int inLen) {
  int bytesReceivedCount = recv(
    mSocket,
    static_cast<void*>(inBuffer),
    inLen,
    0
  );

  if (bytesReceivedCount >= 0)
    return bytesReceivedCount;

  SocketUtil::ReportError("TCPSocket::Recv");
  return -SocketUtil::GetLastError();
}

TCPSocket::~TCPSocket() {
  close(mSocket);
}
```


```cpp
// SocketUtil
TCPSocketPtr SocketUtil::CreateTCPSocket(SocketAddressFamily inFamily) {
  SOCKET s = socket(inFamily, SOCK_STREAM, IPPROTO_TCP);
  if (s != -1)
    return TCPSocketPtr(new TCPSocket(s));

  ReportError("SocketUtil::CreateTCPSocket");
  return nullptr;
}
```


## 블로킹 I/O와 논블로킹 I/O

소켓 관련 함수는 대부분 블로킹 호출이기 때문에 메인스레드에서 소켓으로 패킷을 처리하는 것은 적절하지 않다.

**멀티스레딩**, **논블로킹 I/O**, **`select()`** 를 통해 해결할 수 있다.

### 멀티스레딩

내용 보충 예정

### 논블로킹 I/O

소켓을 논블로킹 모드로 설정하여 블로킹하지 않고 `-1`을 즉시 리턴하도록 만들 수 있다.

에러코드는 `errno`에서 `EAGAIN`, `WSAGetLastError()`에서 `WSAEWOULDBLOCK` 으로 설정된다.

윈도우에서는 `ioctlsocket()`, 리눅스에서는 `fctl()`을 사용한다.

```cpp
// Windows
int ioctlsocket(SOCKET sock, long cm, u_long* argp);

// Linux
#include <fcntl.h>
int fcntl(int sock, int cmd, ...);
```

- `ioctlsocket()`
	- `cmd`: 제어하려는 소켓 파라미터. `FIONBIO`
	- `argp`: 파라미터에 설정하는 값. 0이면 블로킹 모드, 0이 아니면 논블로킹 모드

- `fctl`의 경우 조금 다르게 사용한다.

```cpp
int flags = fcntl(mSocket, F_GETFL, 0);
fcntl(mSocket, F_SETFL, flags | O_NONBLOCK);
```

먼저 `F_GETFL`로 소켓에 원래 플래그를 가져오고, 거기에 `O_NONBLOCK`을 비트 OR 연산한 후 다시 `F_SETFL`로 덮어씌워야 한다.


#### UDPSocket 클래스에 논블로킹 모드 추가

```cpp
// UDPSocket.cpp
int UDPSocket::SetNonBlockingMode(bool isShouldBeNonBlocking) {
  int result;
#if _WIN32
  u_long arg = inShouldBeNonBlocking ? 1 : 0;
  result = ioctlsocket(mSocket, FIONBIO, &arg);
#else
  int flags = fcntl(mSocket, F_GETFL, 0);
  flags = isShouldBeNonBlocking ? (flags | O_NONBLOCK) : (flags | ~O_NONBLOCK);
  result = fcntl(mSocket, F_SETFL, flags);
#endif

  if (result != -1) // SOCKET_ERROR
    return 0;

  SocketUtil::ReportError("UDPSocket::SetNonBlockingMode");
  return SocketUtil::GetLastError();
}
```

### select() 함수

논블로킹 소켓으로 프레임마다 폴링하는 방식은 폴링해야 할 소켓의 수가 많아지면 비효율적이다.
데이터가 오지 않아도 `recv`를 계속 호출하면서 데이터가 왔는지 확인해야 하고, 소켓이 1000개라면 1000번의 시스템 콜을 발생시키는 꼴이다.

`select()`는 I/O Multiplexing 이라고도 하는데, 관심 소켓을 등록해두고, 그 중 하나 이상에 신호가 오면 그 때 처리하도록 한다.

```cpp
// Windows
int select(int nfds, 
			fd_set* readfds,
			fd_set* writefds,
			fd_set* exceptfds,
			const timeval* timeout
);

// Linux
int select(int nfds,
			fd_set* readfds,
			fd_set* writefds,
			fd_set* exceptfds,
			struct timval* timeout
);
```

POSIX 플랫폼에서는 `nfds`에 소켓 식별자 (리눅스에서는 파일 디스크립터의 int값)