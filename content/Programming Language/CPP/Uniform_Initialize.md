---
title: "[C++] Uniform Initialize (유니폼 초기화)"
description: "\bC++11 부터는 유니폼 초기화를 통해 클래스와 구조체를 같은 방법으로 초기화할 수 있다."
draft: false
tags:
  - cpp
  - cpp11
---
# Uniform Initialize

C++11 이전에는 초기화 방법이 일관되지 않았다.

```cpp
struct CircleStruct {
	int x, y;
	double radius;
};

class CircleClass {
  public:
	CircleClass(int x, int y, double radius)
				: mX(x), mY(y), mRadius(radius) {}
	
  private:
	int mX, mY;
	double mRadius;
};
```

위와 같이 원을 정의한 구조체와 클래스가 각각 있을 때,

### C++11 이전

C++11 이전에는 아래와 같이 초기화 했다.

```cpp
CircleStruct structCircle = {10, 10, 2.5}; // 구조체 초기화에서는 {...} 사용
CircleClass classCircle(10, 10, 2.5);      // 클래스 초기화는 함수표기법 (...) 사용
```

### C++11 이후

C++11 이후부터는 중괄호 `{}` 를 사용하여 유니폼 초기화를 따르도록 통일됐다.

```cpp
CircleStruct structCircle1 = {10, 10, 2.5}; 
CircleClass classCircle1 = {10, 10, 2.5};

// 등호 생략도 가능
CircleStruct structCircle2{10, 10, 2.5}; 
CircleClass classCircle2{10, 10, 2.5};
```

중괄호 `{}`를 사용한 초기화는 구조체/클래스 말고도 C++의 모든 대상을 초기화할 수 있다.

```cpp
int a = 3;
int b(3);
int c = {3};
int d{3};

// 제로 초기화
int e{}; // e == 0
```

### Narrowing Conversion (축소 변환) 방지

유니폼 초기화는 **Narrowing Conveersion (축소 변환)** 을 방지할 수 있다.

```cpp
void func(int i) { /* codes */ }

int main() {
	int x = 3.14;
	func(3.14);
}
```

변수 `x`에 `3.14`를 대입할 때나 `func()` 의 인자로 `3.14`를 전달할 때 값이 3으로 줄어든다. 

유니폼 초기화를 사용하면 해당 부분에 에러 메시지를 생성한다.

```cpp
int main() {
	int x = {3.14};
	func({3.14});
}
```

### 유니폼 초기화로 동적 할당 배열 초기화

```cpp
int* pArr = new int[4]{0, 1, 2, 3};
```

### 클래스 멤버 배열을 [생성자 이니셜라이저](Member_Initializer_List) 로 초기화

```cpp
class MyClass {
  public:
	  MyClass() : mArray{0, 1, 2, 3} {}
	  
  private:
	  int mArray[4];
};
```


---

## 직접 리스트 초기화와 복제 리스트 초기화

- copy list initialization: `T obj = {arg1, arg2, ...}`
- direct list initialization: `T obj {arg1, arg2, ...}`


C++17 이전에는 복제 리스트 / 직접 리스트 초기화 모두 `initializer_list<>` 로 처리했다.

```cpp
// 복제 리스트 초기화
auto a = {11};     // initializer_list<int>
auto b = {11, 22}; // initializer_list<int>

// 직접 리스트 초기화
auto c {11};     // initializer_list<int>
auto d {11, 22}; // initializer_list<int>
```


#cpp17 부터는 직접 리스트 초기화에서 `auto`는 값 하나만 추론한다.

```cpp
// 복제 리스트 초기화
auto a = {11};     // initializer_list<int>
auto b = {11, 22}; // initializer_list<int>

// 직접 리스트 초기화
auto c {11};     // int
auto d {11, 22}; // 에러: 원소가 많음
```

