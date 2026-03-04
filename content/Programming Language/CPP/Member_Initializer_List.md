---
title: "[C++] ctor initializer (생성자 이니셜라이저)"
description: const 멤버나 기본 생성자가 없는 멤버 등에는 Initializer List를 사용해 초기화한다.
draft: false
tags:
  - cpp
---
# 생성자 이니셜라이저

생성자로 데이터 멤버를 초기화 하는 방법은 두가지가 있다.

- 생성자 본문 `{}` 안에서 초기화
- ctor (생성자) 이니셜라이저를 통한 초기화

생성자 본문에서 값을 대입할 때는 먼저 멤버가 디폴트 값으로 생성된 후에 값을 수정하는 두 단계를 거쳐야 하지만, 이니셜라이저를 사용하면 생성과 동시에 초기화되기 때문에 효율적이다.

또 클래스 타입의 멤버 변수가 있을 때는 본문에서 대입할 때는 대입 연산자가 호출되지만 이니셜라이저 사용시에는 **복사 생성자**가 호출되어 성능 향상을 꾀할 수 있다.

생성자 이니셜라이저로 멤버 변수를 초기화하려면, 생성자 이름 뒤에 콜론 `:` 을 붙여 표현한다.

```cpp
class MyClass {
public:
	MyClass();
	
private:
	int mInt;
	string mString;
	bool mBool;
};

// 생성자 이니셜라이저
MyClass::MyClass()
	: mInt(10)
	, mString("Initial String");
	, mBool(true)
	{}
```



### 반드시 생성자 이니셜라이저를 사용해야 하는 경우

- `const` 멤버

```cpp
class MyClass {
	const int mId;
	
public:
	MyClass(int id) : mId(id) {}
};
```

- 레퍼런스 (참조) `&` 멤버

```cpp
class MyClass {
	int& mRef;
	
public:
	MyClass(int& ref) : mRef(ref) {}
};
```

- 디폴트 생성자가 없는 객체의 멤버

```cpp
class Bar {
public:
	Bar(int x) {} // 기본 생성자 없음
};

class Foo {
	Bar bar;
public:
	Foo(): bar(42) {} // 필수임!
};
```

- 부모 클래스의 생성자 호출 (생성자 체이닝)

```cpp
class Parent {
	std::string mName;
	
public:
	Parent(std::string name) : mName(name) {}
};

class Child : public Parent {
	int mAge;
	
public:
	Child(std::string name, int age)
		: Parent(name)
		, mAge(age)
		{}
};
```

## 초기화 시 순서 주의사항

초기화 순서는 Initializer List 순서가 아니라 클래스 내 멤버 선언 순서를 따른다는 것을 명심해야 한다.

```cpp
class Foo {
	int a;
	int b;
public:
	Foo(int x) : b(x), a(b) {} // a가 먼저 초기화 되는데, b는 아직 쓰레기 값이라 버그 발생
};


class Foo {
	int a;
	int b;
	
public:
	Foo(int x) : a(x), b(a) {} // 멤버 선언 순서와 일치
};
```

## 생성자 위임

```cpp
class Foo {
	int mX, mY;
	std::string mName;
	
	Foo(int x, int y, std:;string name) : mX(x), mY(y), mName(name) {
		// 공통 초기화 로직
	}
public:
	Foo() : Foo(0, 0, "default string") {}
	Foo(int x, int y) : Foo(x, y, "none") {}
};
```

