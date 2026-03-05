---
title: "[C++] string과 string_view"
description: "\bC스타일 스트링과 std::string, std::string_view 를 알아본다."
draft: false
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

```cpp
char* a = "12";
char b[] = "12";
```

위 두 스트링을 비교하려고 할 때, `a==b`  처럼 작성하면 스트링의 내용이 아니라 포인터 값을 비교하기 때문에 무조건 `false`가 리턴된다. `==` 대신, `strcmp()` 함수로 스트링을 비교해야만 한다.

```cpp
if (strcmp(a, b) == 0) {} // 같으면 0, 다르면 -1 또는 1
```

`string`은 `==`, `!=`, `<` 같은 연산자들을 오버로딩해서 스트링 연산에 적용할 수 있다.
메모리 관련 작업도 string 클래스가 알아서 처리해주기 때문에 편리하다.

`string`에서 제공하는 `c_str()` 메서드를 사용하면 C 언어와의 호환성을 보장할 수 있다.

`c_str()`은 C 스타일 스트링을 표현하는 `const char *` 를 리턴한다. 주의할 점은, string에 대한 메모리를 재할당하거나 string 객체를 제거하게 되면 `c_str()`로 리턴한 포인터를 사용할 수 없게 되므로, 메서드 호출 직후에 포인터를 활용하도록 해야 한다.

`data()` 메서드는 C++14 까지는 `c_str()`과 같이 `const char*` 로 값을 리턴했지만, #cpp17
 부터는 **non-const** 스트링에 대해 호출하면 `char*`을 리턴한다.

#### std::string 리터럴

스트링 리터럴은 주로 `const char*`로 처리하는데, `'s'` 를 사용하면 스트링 리터럴을 `std::string`으로 만들 수 있다.

```cpp
auto strgin1 = "Hello World";  // const char*
auto string2 = "Hello World"s; // std::string
```

`'s'`를 사용하려면 `using namespace std::string_literals;` 혹은 `using namespace std;` 를 추가해야 한다.


#### 하이레벨 숫자 변환

숫자와 스트링을 쉽게 변환하는 헬퍼 함수가 존재한다.

```cpp
string to_string(int val);

string to_string(unsigned val);

string to_string(long val);

// 이외에도 다양한 타입에 대한 변환 함수 ...
```

`to_string()`은 string 객체를 새로 생성해서 리턴한다.

반대로 스트링을 숫자로 변환하는 함수도 있다.

```cpp
int stoi(const string& str, size_t *idx=0, int base=10);

long stol(const string& str, size_t *idx=0, int base=10);

unsigned long stoul(const string& str, size_t *idx=0, int base=10);

long long stoll(const string& str, size_t *idx=0, int base=10);

unsigned long long stoull(const string& str, size_t *idx=0, int base=10);

float stof(const string& str, size_t *idx=0, int base=10);

double stod(const string& str, size_t *idx=0, int base=10);

long double stold(const string& str, size_t *idx=0, int base=10);
```

`str`은 변환할 원본 스트링, `idx`는 아직 변환되지 않은 부분의 맨 앞 문자의 인덱스를 가리키는 포인터, `base`는 변환할 수의 밑 (base) 이다.

위 변환 함수들은
- 맨 앞의 공백 문자를 무시한다.
- 변환 실패 시 `invalid_argument` 익셉션을 던진다.
- 변환된 값이 리턴 타입의 범위를 벗어나면 `out_of_range` 익셉션을 던진다.


#### 로우레벨 숫자 변환

#cpp17 부터는 `<charconv>` 헤더로 로우레벨 숫자 변환 메서드를 다양하게 지원한다.

메모리 할당 관련 작업은 안해주기 때문에 호출 측에서 버퍼를 할당하는 식으로 사용해야 한다.

동적할당, 예외처리 등이 없기 때문에 고성능이고, **로케일 독립성**을 가진다.

정수를 문자로 변환할 때는 `to_chars()` 함수를 사용한다.

```cpp
to_chars_result to_chars(char* first, char* last, IntegerT value, int base=10);
```

`IntegerT`에는 signed 정수, unsigned 정수, char 가 나올 수 있다.

`to_chars_result` 타입으로 리턴된다.

```cpp
struct to_chars_result {
	char* ptr;
	errc ec;
};
```

정상적으로 변환 됐다면 `ptr` 멤버는 끝에서 두 번째 문자를 가리키고, 그렇지 않으면 `last`와 같은 값이다.
(`ec == errc::value_too_large`)

아래는 사용 예시이다.

```cpp
std::string out(10, ' ');
auto result = std::to_chars(out.data(), out.data() + out.size(), 12345);
// 혹은 구조적 바인딩: auto [ptr, ec] = std::to_chars(...);
if (result.ec == std::errc()) { /* 제대로 변환된 경우 */}
```

이외에도 부동 소수점 타입 변환 함수도 있다.

```cpp
to_chars_result to_chars(char* first, char* last, FloatT value);
to_chars_result to_chars(char* first, char* last, FloatT value
						, chars_format format);
to_chars_result to_chars(char* first, char* last, FloatT value
						, chars_format format, int precision);
```

```cpp
enum class chars_format {
	scientific,
	fixed,
	hex,
	general = fixed | scientific
};
```

`chars_format` 플래그를 조합해서 부동소수점 타입의 포맷의 정할 수 있다.

<br>

스트링을 숫자로 변환할 수 있다.

```cpp
from_chars_result from_chars(const char* first, const char* last,
							IntegerT& value, int base=10);

from_chars_result from_chars(const char* first, const char* last,
							FloatT& value,
							chars_format format = chars_format::general);
```

```cpp
struct from_chars_result {
	const char* ptr;
	errc ec;
};
```

- `ptr`은 변환 실패할 경우에 첫 번째 문자에 대한 포인터, 제대로 변환 될 때 `last`와 같다 (복잡하다;)

- 변환된 문자가 하나도 없다면 `ptr`은 `first`와 같고 에러코드는 `errc::invalid_argument`가 된다.

- 파싱된 값이 지정된 타입 범위보다 크면 `errc::result_out_of_range`가 된다.

- `from_chars()`는 앞에 나온 공백을 무시하지 않는다. (`to_chars()`는 무시함)


### std::string_view 클래스
#cpp17

C++17이전에는 **읽기 전용 스트링을 받는 함수**의 매개변수 타입을 정할 때 문제가 있었다.

```cpp
// 읽기 전용 함수 매개변수가 const std::string& 인 경우
void print(const std::string& str) { std::cout << str; }

// 읽기 전용 함수 매개변수가 const char* 인 경우
void print(const char* str) { std::cout << str; }
```

위 예시에서 `print()` 의 매개변수를 `const string&`로 해야하는지, `const char*`로 해야하는지 결정하기 힘들다.

- `const char*` 로 하면:
매개 변수로 `std::string`을 `c_str()`이나 `data()`를 통해 한번 변환하는 과정이 필요하다.

- `const std::string&`로 하면

```cpp
const char* cstr = "hi";

print(cstr);
print("hi"); // 힙 할당 발생 오버헤드!!
```

스트링 리터럴이나 `const char*` 을 매개변수로 전달했을 때 임시 `std::string` 객체를 생성하여 리터럴이 복사되는 오버헤드가 발생한다. `std::string_view`를 사용하여 이러한 문제를 해소할 수 있다.

<br>

`string_view`는 `c_str()` 이 없다는 점을 제외하고 `std::string`과 같다. 
추가적으로 `remove_prefix(size_t)`, `remove_suffix(size_t)` 메서드로 오프셋만큼 스트링의 시작/끝 포인터를 앞으로 당기기/밀기 가능하다. (스트링 축소)

`string`과 `string_view`는 서로 concatenating 할 수 없다.

```cpp
string str = "Hello";
string_view sv = " world";

// auto result = str + sv;    ---->    컴파일 에러!
auto result = str + sv.data();    // c_str() 은 없으나 data() 는 있음
```

`string_view`는 레퍼런스보다 값으로 전달하는 경우가 많다.
스트링 포인터와 길이만 유지하기 때문에 복사 오버헤드가 적다.

```cpp
string_view extractExtension(string_view fileName) {
	return filename.substr(fileName.rfind('.'));
}
```

위처럼 정의된 함수를 사용하면 매개변수 호출 시 복제 연산이 일어나지 않는다!

```cpp
std::string fileName = R"(c:\temp\my file.txt)";
std::cout << "C++ string: " << extractExtension(fileName) << std::endl;

const char* cString = R"(c:\temp\my file.txt)";
std::cout << "C string: " << extractExtension(fileName) << std::endl;

std::cout << "Literal: " << extractExtension(R"(c:\temp\my file.txt)") << std::endl;
```


<br>

`string_view` 생성자 중 원시 `char*` 버퍼와 길이를 받는 형태가 있다.

```cpp
string_view(const char* ptr, size_t len);
```

`NUL`로 끝나지 않는 스트링 버퍼로 `string_view`를 생성할 수 있다.

사용 예시는 아래와 같다.

```cpp
const char* buf = "Hello World";

std::string_view sv1(buf, 5); // "Hello"

std::string_view sv2(buf + 6, 5); // "World"
```

`string_view`로  `string`를 생성하려면 `string_view::data()` 를 사용하면 된다.


#### std::string_view 리터럴
`'sv'` [[#std string 리터럴]] 에서 `'s'`를 사용한 것처럼 스트링 리터럴을 `string_view`로 만들 수 있다.

`'sv'`를 사용하려면 `using namespace std::string_view_literals;` 를 추가해야 한다.
