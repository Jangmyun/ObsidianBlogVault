---
title: "[C++] Template (템플릿)"
description: 타입을 매개변수로 받아 함수/클래스를 일반화하는 템플릿 문법 정리.
draft: false
tags:
  - cpp
---
# Template (템플릿)

템플릿은 타입을 매개변수처럼 받아서 함수나 클래스를 **일반화**할 수 있게 해주는 기능이다.

같은 로직을 `int`, `double`, `std::string` 등 여러 타입에 대해 반복해서 작성하는 대신, 템플릿으로 한 번만 작성하고 컴파일러가 실제로 사용되는 타입에 맞춰 코드를 생성하게 할 수 있다.

## 함수 템플릿 (Function Template)

```cpp
template <typename T>
T myMax(T a, T b)
{
	return (a > b) ? a : b;
}
```

`typename` 대신 `class` 키워드를 써도 동일하게 동작한다.

```cpp
template <class T>
T myMax(T a, T b) { return (a > b) ? a : b; }
```

### 템플릿 인자 추론

함수 템플릿을 호출할 때 인자의 타입을 보고 컴파일러가 `T`를 자동으로 추론한다. 명시적으로 타입을 지정할 수도 있다.

```cpp
myMax(3, 7);        // T = int, 자동 추론
myMax(3.5, 2.1);     // T = double, 자동 추론
myMax<double>(3, 7); // T를 명시적으로 지정
```

두 인자의 타입이 다르면 추론에 실패해서 컴파일 에러가 발생한다.

```cpp
myMax(3, 7.5); // 에러! T가 int인지 double인지 추론 불가
```

### 여러 타입 매개변수

템플릿 매개변수는 여러 개를 받을 수 있다.

```cpp
template <typename T, typename U>
void printPair(T a, U b)
{
	std::cout << a << ", " << b << std::endl;
}

printPair(1, "hello"); // T = int, U = const char*
```

## 클래스 템플릿 (Class Template)

클래스도 템플릿으로 작성해서 여러 타입에 대해 동작하는 자료구조를 만들 수 있다.

```cpp
template <typename T>
class Stack
{
public:
	void push(const T& value);
	T pop();
	bool isEmpty() const;

private:
	std::vector<T> mElements;
};
```

클래스 템플릿을 사용할 때는 타입을 명시적으로 지정해야 한다 (함수 템플릿과 달리 인자로부터 추론할 수 없기 때문).

```cpp
Stack<int> intStack;
Stack<std::string> stringStack;
```

### 멤버 함수를 클래스 밖에서 정의

멤버 함수를 클래스 정의 밖에서 구현할 때는 `template` 선언과 `Stack<T>::` 형태의 범위 지정이 매번 필요하다.

```cpp
template <typename T>
void Stack<T>::push(const T& value)
{
	mElements.push_back(value);
}

template <typename T>
T Stack<T>::pop()
{
	T top = mElements.back();
	mElements.pop_back();
	return top;
}
```

### 기본 템플릿 인자

함수의 디폴트 인자처럼, 템플릿 매개변수에도 기본값을 지정할 수 있다.

```cpp
template <typename T = int>
class Container
{
	T mValue;
};

Container<> c; // T = int, 기본값 사용
```

## 템플릿 특수화 (Template Specialization)

특정 타입에 대해서는 일반적인 템플릿과 다르게 동작해야 할 때 **특수화**를 사용한다.

### 전체 특수화 (Full Specialization)

```cpp
template <typename T>
class Formatter
{
public:
	std::string format(T value) { return std::to_string(value); }
};

// bool 타입에 대한 전체 특수화
template <>
class Formatter<bool>
{
public:
	std::string format(bool value) { return value ? "true" : "false"; }
};
```

`Formatter<bool>` 을 사용하면 일반 템플릿 대신 특수화된 버전이 선택된다.

함수 템플릿도 동일한 방식으로 전체 특수화할 수 있다.

```cpp
template <typename T>
void printType() { std::cout << "generic" << std::endl; }

template <>
void printType<int>() { std::cout << "int" << std::endl; }
```

### 부분 특수화 (Partial Specialization)

템플릿 매개변수 중 일부만 고정하는 **부분 특수화**는 클래스 템플릿에만 사용할 수 있다 (함수 템플릿은 불가능).

```cpp
template <typename T, typename U>
class Pair
{
	// 일반적인 경우
};

// U가 항상 int인 경우로 부분 특수화
template <typename T>
class Pair<T, int>
{
	// T, int 조합에 대한 특수화
};

// 두 타입이 포인터인 경우로 부분 특수화
template <typename T, typename U>
class Pair<T*, U*>
{
	// 포인터 조합에 대한 특수화
};
```

## Non-type 템플릿 매개변수

타입이 아니라 **값**을 템플릿 매개변수로 받을 수도 있다. 대표적으로 `std::array` 의 크기가 이 방식으로 구현되어 있다.

```cpp
template <typename T, std::size_t N>
class FixedArray
{
public:
	T& operator[](std::size_t index) { return mData[index]; }

private:
	T mData[N];
};

FixedArray<int, 10> arr; // N = 10
```

Non-type 매개변수로는 정수, 열거형, 포인터, 참조 등 컴파일 타임에 값이 결정되는 타입만 사용할 수 있다.

## 헤더에 구현까지 작성해야 하는 이유

템플릿은 실제로 사용되는 타입이 정해져야 컴파일러가 코드를 생성할 수 있다 (**암시적 인스턴스화**). 그래서 템플릿 함수/클래스의 구현을 `.cpp` 파일에 분리해두면, 다른 `.cpp` 파일에서 그 템플릿을 사용할 때 링커가 실제 구현을 찾지 못해 링크 에러가 발생한다.

이런 이유로 템플릿은 보통 선언과 구현을 모두 헤더 파일에 작성한다.
