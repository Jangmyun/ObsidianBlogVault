---
title: "[C++] std::optional"
description: 값이 있을 수도 없을 수도 있는 상태를 표현할 때 사용하는 std::optional 사용법.
draft: false
tags:
  - cpp
---
# std::optional

`std::optional<T>` 은 값이 **있을 수도, 없을 수도** 있는 상태를 표현하는 타입이다. `<optional>` 헤더에 정의되어 있다.

값이 없는 상태를 `nullptr` 이나 별도의 `bool` 플래그, 혹은 매직 넘버 (예: `-1`) 로 표현하던 것을 대체할 수 있어서, 아래와 같은 상황에 유용하다.

- 아직 초기화되지 않았을 수도 있는 데이터 멤버
- 실패할 수도 있는 함수의 반환값 (예외를 던지기엔 과한 경우)
- "설정 안 함" 을 표현해야 하는 함수 인자

예를 들어 `std::string` 데이터 멤버를 그냥 두면 기본 생성자가 호출되어 빈 문자열 `""` 상태가 되는데, 이는 "빈 문자열 값이 설정됨" 과 "아직 값이 설정되지 않음" 을 구분할 수 없다. `std::optional<std::string>` 을 사용하면 두 상태를 명확히 구분할 수 있다.

## 생성과 대입

```cpp
std::optional<int> a; // 기본 생성 시 값 없음 (empty)
std::optional<int> b = std::nullopt; // 명시적으로 값 없음을 표현

std::optional<int> c = 42; // 값을 가진 상태로 생성
std::optional<int> d = std::make_optional(42); // 위와 동일

a = 10; // 값 대입
```

## 값이 있는지 확인

`has_value()` 를 사용하거나, `optional` 자체를 `bool` 로 변환해서 확인할 수 있다.

```cpp
if (a.has_value()) { /* ... */ }
if (a) { /* ... */ } // 위와 동일
```

## 값 꺼내기

- `value()` : 값이 있으면 반환, 없으면 `std::bad_optional_access` 익셉션 발생
- `operator*`, `operator->` : 값이 있다고 가정하고 바로 접근 (없으면 UB)
- `value_or(default)` : 값이 있으면 그 값을, 없으면 인자로 넘긴 기본값을 반환

```cpp
std::optional<std::string> name;

std::string s1 = name.value();       // 값이 없으면 예외 발생
std::string s2 = *name;              // 값이 없으면 UB
std::string s3 = name.value_or("");  // 값이 없으면 "" 반환
```

## 값 비우기

값을 비우려면 `reset()` 을 호출하거나 `std::nullopt` 을 대입한다.

```cpp
a.reset();
a = std::nullopt;
```

## emplace() 로 직접 생성

`emplace()` 를 사용하면 대입 대신 `optional` 내부에서 객체를 직접 생성할 수 있어, 임시 객체 생성/복사를 피할 수 있다.

```cpp
std::optional<std::string> str;
str.emplace(5, 'a'); // std::string(5, 'a') 를 직접 생성 -> "aaaaa"
```

## 비교 연산

`optional` 끼리, 혹은 `optional` 과 값을 직접 비교할 수 있다. 값이 없는 상태는 값이 있는 어떤 상태보다도 작은 것으로 취급된다.

```cpp
std::optional<int> a = 1;
std::optional<int> b = std::nullopt;

a == 1;      // true
a > b;       // true, 값이 있는 쪽이 더 큼
b < a;       // true
```
