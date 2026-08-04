---
title: "[C++] 예외 대신 assert로  반복 연산 구간을 효율적으로 방어하기"
description: 성능이 중요한 반복 호출 구간에서 예외 대신 assert로 버그를 잡는 법
draft: false
tags:
  - cpp
---
# assert vs 예외

함수에 잘못된 값이 들어왔을 때 막는 방법은 크게 두 가지다. **예외(exception)**와 **assert**.

둘의 역할이 다르다는 걸 먼저 구분해야 한다.

- **예외**: 런타임에 실제로 일어날 수 있는 상황을 처리 (사용자 입력 오류, 파일 없음, 네트워크 실패 등)
- **assert**: 프로그래머의 실수를 잡는 용도 (여기 도달하면 안 되는데 도달했다 = 버그)

`operator[]`에 잘못된 index가 들어오는 경우는 사용자 입력 문제가 아니라 **코드 짜는 사람의 실수**에 가깝다. 그래서 이런 경우엔 예외보다 assert가 더 맞는 선택이 될 때가 많다.

## 왜 반복 연산 구간에서는 assert가 유리한가

`Vector`, `Matrix` 같이 반복문 안에서 수만~수억 번 호출되는 연산에 매번 `if` 체크 + `throw`를 넣으면 그 자체로 오버헤드다. 여기서 assert의 특성이 빛을 발한다.

```cpp
#include <cassert>

double Vec2::operator[](int index) const {
  assert(index == 0 || index == 1);
  return index == 0 ? x : y;
}
```

이 코드는 **빌드 모드에 따라 완전히 다르게 동작한다.**

|빌드 모드|assert 동작|
|---|---|
|디버그 (`NDEBUG` 미정의)|조건이 거짓이면 즉시 프로그램 중단 + 어느 파일/라인인지 출력|
|릴리즈 (`-DNDEBUG`)|통째로 사라짐 — 코드가 아예 없는 것처럼 컴파일됨|

즉 개발 중에는 버그를 바로 잡아주고, 실전 배포 시에는 오버헤드가 **0**이 된다. 예외처럼 항상 살아있는 방어 코드가 아니라, "개발할 때만 켜지는 안전벨트"인 셈이다.

### 실제로 확인해보기

```cpp
int main() {
  Vec2 a(1.0, 2.0);
  std::cout << a[5] << "\n"; // 범위 밖 index
}
```

```bash
# 디버그 빌드
g++ -std=c++17 main.cpp -o debug
./debug
# → Assertion `index == 0 || index == 1' failed. Aborted (core dumped)

# 릴리즈 빌드
g++ -std=c++17 -DNDEBUG main.cpp -o release
./release
# → 2  (그냥 y값을 조용히 반환하고 넘어감)
```

릴리즈 빌드에서 assert가 사라진다는 걸 직접 확인해두면, "왜 배포 버전에서는 이 체크가 안 먹히지?" 하는 삽질을 미리 방지할 수 있다.

## 바로 쓰는 템플릿

```cpp
#include <cassert>

// 반환값이 있는 경우
T MyClass::operator[](int index) const {
  assert(index >= 0 && index < SIZE && "index out of range");
  return data[index];
}

// void 함수인 경우
void MyClass::setValue(int index, T value) {
  assert(index >= 0 && index < SIZE && "index out of range");
  data[index] = value;
}
```

`assert(조건 && "메시지")` 형태로 쓰면 실패했을 때 메시지도 함께 출력되어 디버깅이 훨씬 편해진다. (`&&`가 항상 `true`인 문자열 포인터와 논리곱을 하는 트릭이라 조건에는 영향 없음.)

## 언제 assert를 쓰면 안 되나

- **사용자 입력을 직접 검증할 때** → 릴리즈에서 사라지므로 절대 안 됨. 예외나 반환값 체크 사용.
- **호출 빈도가 낮고 안전이 중요한 API 경계** (라이브러리 공개 인터페이스 등) → 예외가 더 적합.

정리하면: **"여기 도달하면 무조건 내 코드가 잘못된 것"**이라고 확신할 수 있는 곳, 그리고 **성능이 중요한 반복 구간**에서 assert를 쓴다. 그 외에는 예외.


