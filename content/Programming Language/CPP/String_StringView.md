---
title: "[C++] string과 string_view"
description: Example Description
draft: true
tags:
  - cpp
---
## 동적 스트링

### C 스타일 스트링

C언어는 기본적으로 문자 배열 (Char Array) 로 스트링을 표현한다. 스트링의 마지막에 널 `NUL` 문자 `'\0'` 를 붙여서 스트링의 끝임을 표현한다. (`NULL` 아님 주의)

스트링을 다룰 때 메모리 공간에 항상 `\0` 을 위한 자리가 필요하다는 사실을 잊으면 안된다.

C++에서는 `<cstring>` 헤더 파일을 통해 C에서 사용하던 스트링 연산 함수들을 제공한다.
`<cstring>`에 정의된 함수들은 대체로 메모리 할당 기능을 제공하지 않는 경우가 많다.

```cpp
char* copyString(const char* str) {
	char* result = new char[strlen(str) + 1]; // strlen(str)은 '\0'을 포함안함 주의
	strcpy(result, str);
	return result;
}
```

`strcpy()` 의 경우, 인자로 받은 두 스트링 중 두 번째를 첫 번째 스트링에 복사한다. 문자열의 길이가 같은지는 확인하지 않기 때문에 주의가 필요하다.

스트링 길이를 확인하는 `strlen()` 함수의 경우에는 메모리 크기가 아니라 스트링 길이를 리턴하기 때문에 널 문자를 위한 자리를 추가하기 위해 `strlen(str) + 1` 로 복사할 `result` 문자열의 길이를 지정해야한다.

그냥 메모리 길이만큼 바로 리턴해주면 되는 것이 아닌가 생각할 수 있지만, 여러 개의 문자열을 이어 붙이는 경우에 문제가 생길 수 있다.

```cpp
char* appendStrings(const char* str1, const char* str2) {
	char* result = new char[strlen(str1) + strlen(str2) + 1];
	strcpy(result, str1);
	strcat(result, str2);
}
```

위와 같은 경우에 `strlen()` 의 결과가 `'\0'` 를 포함하도록 구현됐다면 메모리 공간에 맞게 스트링 길이를 계산하기 번거롭다.

`sizeof()` 연산자로 데이터 타입 혹은 변수 크기를 구할 수 있는데, C 스타일 스트링의 경우 `strlen()`과 `sizeof()`의 결과가 다르니 스트링 길이를 구할 때는 `sizeof()`를 사용하면 안된다.
특히, C 스타일 스트링을 `char[]` 가 아니라 `char*`로 저장한 경우 `sizeof()`의 결과는 "포인터" 의 크기를 반환한다.

```cpp
char text1[] = "abcde";
size_t textSizeof = sizeof(text1); // 6
size_t textStrlen = strlen(text1); // 5

const char* text2 = "abcde";
size_t textSizeof2 = sizeof(text2); // 플랫폼마다 다름
size_t textStrlen2 = strlen(text2); // 5
```


C스타일 스트링 함수 사용 시 보안 관련하여 경고나 에러메시지가 출력될 수 있는데, `strcpy_s()`, `strcat_s()` 등 길이를 명시하는 secure C 언어 라이브러리를 사용하면 된다. (근데 사실 `string` 을 사용하는게 마음 편하다)

### 스트링 리터럴

```cpp
cout << "hello" << endl;
```

위 코드에서 `hello` 처럼 변수에 담지 않고 바로 값으로 표현한 스트링을 **스트링 리터럴** 이라고 부른다.


#### 리터럴 풀링 

스트링 리터럴은 메모리의 **읽기 전용 영역**에 저장되고, 코드에 같은 스트링 리터럴이 여러번 등장하면 그중 한 스트링에 대한 레퍼런스를 **재사용**하여 메모리를 절약한다. 이를 ***Literal Pooling (리터럴 풀링)*** 이라고 한다.


#### Raw String Literal

#cpp11 부터 도입된 기능으로, 이스케이프 시퀀스 (ex. `\t`, `\n`)를 무시하는 문자열 리터럴이다.

```cpp
R"(문자열 내용)"
```

기본 문법은 `R"(` 로 시작해서 `)"` 로 끝난다.

```cpp
const char* str = R"(Hello "World"!)";
```

이러면 일반 스트링에서 선언 한 것처럼 `"Hello \"World\"!"`  같이 이스케이프 시퀀스 표현을 하지 않아도 되기 때문에 편리하다. 뿐만 아니라 `\n` 을 직접 입력할 필요 없이 그냥 엔터키를 눌러서 `\n` 을 지정했을 때와 같은 출력을 만들 수 있다.

`)"`로 끝나기 때문에 중간에 `)"` 가 들어올 수 없다는 점은 주의해야 한다.

`)"` 가 포함되어야 할때는 구분자를 지정해야 한다.

```cpp
R"d-char-sequence(이 안에서는 가능)d-char-sequence"
```

`d-char-sequence` 라고 표현된 부분이 구분자 시퀀스이다. 구분자 시퀀스도 마찬가지로 스트링 리터럴 안에는 등장하면 안된다.

아래는 또다른 예시이다.

```cpp
const char* str = R"-(Embedded )" characters)-";
```

스트링 리터럴을 잘 활용해서 DB 쿼리나 정규표현식, 파일 경로등을 쉽게 표현할 수 있다.


### std::string 클래스

C++ 에서는 스트링을 쉽게 사용할 수 있는 `std::string` 클래스를 제공한다. `<string>` 헤더에 정의되어 있다.

#### string 클래스 사용법

`string`은 클래스지만 기본 타입처럼 사용할 수 있다.
연산자 오버로딩을 사용해서 `+`연산자에는 string concatenation, `=` 연산자에는 스트링을 복사하도록 하는 등

