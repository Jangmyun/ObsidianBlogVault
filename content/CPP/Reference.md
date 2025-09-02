---
title: "[C++] Reference"
description:
draft: false
tags:
  - cpp
---
 
포인터와 참조자의 차이점은 포인터는 `NULL`이 될 수 있지만 참조자는 존재하는 것만 지정 가능

```cpp
  int a = 3;
  int &ref_a = a;

  ref_a = 4;
  std::cout << "a : " << a << std::endl;
  std::cout << "ref_a : " << ref_a << std::endl;
```

위 코드 실행의 결과는 

```
a : 4
ref_a : 4
```

`int &ref_a = a`의 뜻은 `ref_a`는 `a`의 참조자임을 알 수 있음
-> `ref_a`는 `a`의 또다른 이름임

**한번 선언된 참조자를 다른 객체를 가리키도록 할 수 없음**


## lvalue 참조자

주로 함수 파라미터의 자료형을 참조자로 하여 객체 복사 없이 사용할 수 있다.

`const`로 lvalue 참조자를 정의한 경우 리터럴 대입 (임시 객체 사용)이 가능하다

```cpp
const int& r1 = 1; // ok
int& r2 =1 // error
```

```cpp
void func_ref(int& n) {}
void func_const_ref(const int& n) {}

int n = 1;
func_ref(n); // ok
func_const_ref // ok

func_ref(1); // error
func_const_ref(1); // ok
```

