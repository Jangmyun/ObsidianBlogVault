---
title: "[C++] Operator Overloading (연산자 오버로딩)"
description: C++의 연산자 오버로딩을 알아보자
draft: false
tags:
  - cpp
---
# Operator Overloading (연산자 오버로딩)


> 내가 만든 클래스로 기본 연산 자를 사용해 연산해보자.

연산자 오버로딩은 C++11 이후로 지원하는 기능으로 `+`, `-`, `==`, `[]` 등 연산자를 사용자 정의 타입 (클래스) 에서 새로운 의미로 재정의할 수 있는 기능을 말한다.

연산자 오버로딩의 문법은 아래와 같다:

```cpp
(리턴 타입) operator(연산자) (연산자가 받는 인자)
```

예시:

```cpp
class Complex {
public:
	double real, img;
	Complex(double r=0, double i = 0): real(r), img(i) {}
};

Complex c1(1, 2), c2(3, 4);

Complex c3 = c1 + c2; // 원래는 불가능하다.
```

참고로 `Complex(double r=0, double i = 0): real(r), img(i) {}` 는 [[Member_Initializer_List]] 를 사용한 초기화 방식이다.

```cpp
// + 연산자를 Complex에 맞게 오버로딩
Complex Complex::operator+(const Complex& other) const {
	return Complex(real + other.real, img + other.img)
}

Complex c3 = c1 + c2; // 가능!
```

연산자는 클래스의 멤버 함수, 전역 함수 두가지 방식으로 오버로딩 할 수 있다.

**전역 함수**로 오버로딩한 경우는 아래와 같다:

```cpp
Complex operator+(const Complex& a, const Complex& b) {
	return Complex(a.real + b.real, a.img + b.img);
}
```

아래 연산자들은 멤버함수로만 오버로딩 가능하다.

```cpp
class Foo {
public:
    // 이들은 멤버 함수만 가능
    Foo& operator=(const Foo& other);      // 대입
    Foo& operator+=(const Foo& other);     // 복합 대입
    Foo& operator++();                     // 전위 증가
    Foo operator++(int);                   // 후위 증가
    Foo& operator--();
    Foo operator--(int);
    Foo& operator[](int index);            // 첨자
    Foo* operator->();                    // 포인터 멤버 접근
    Foo& operator*();                      // 역참조
    // () 호출 연산자
    void operator()(int x);
    // 타입 변환
    operator int() const;
};
```


연산자 오버로딩을 하다보면 예외처리가 필요할 때가 있다. 
예를들어 `[]` 를 통한 인덱싱이 필요한데, 그것이 0과 1, 혹은 작은 숫자 내에서 분기해야 하는 경우가 있다. 정한 범위 밖의 인덱스로 접근하게 되면 예외를 던져야 하는데, 같은 연산이 매우 많이 발생하는 경우 [[Assert]] 를 사용하는 것이 나을 수 있다.