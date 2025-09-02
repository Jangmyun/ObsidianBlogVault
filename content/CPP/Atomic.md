---
title: "[C++] Atomic"
description: Example Description
draft: true
tags:
  - cpp
---
 
## `std::atomic`

여러 스레드가 동시에 안전하게 접근하고 수정할 수 있는 원자적 연산을 제공

## 왜 원자적 연산이 필요한가?

[씹어먹는 C++ - <15 - 3. C++ memory order 와 atomic 객체>](https://modoocode.com/271)


## Atomicity 원자성

원자적 연산이 아닌 경우에 모든 스레드에서 같은 수정 순서를 보장하지 않기 때문에 직접 적절한 동기화 처리가 필요하다.

원자적 연산이란, 중간에 다른 스레드가 끼어들어 값을 수정하거나 참조할 여지가 없는 연산이다. **(쪼갤 수가 없는 연산이다.)**

### Example

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

void worker(std::atomic<int>& counter) {
  for (int i = 0; i < 10000; i++) {
    counter++;
  }
}

int main() {
  std::atomic<int> counter(0);

  std::vector<std::thread> workers;
  for (int i = 0; i < 4; i++) {
    workers.push_back(std::thread(worker, ref(counter)));
  }

  for (int i = 0; i < workers.size(); i++) {
    workers[i].join();
  }

  std::cout << "Counter : " << counter << '\n';
}
```

위 코드를 실행하면 `Counter : 40000`이 된다.

각 worker 스레드의 counter 증가 연산이 atomicity를 보장함을 알 수 있다.

### 원자적 연산 가능 여부 확인

```cpp
std::atomic<int> x;
std:cout << "is lock free ? : " << boolalpha << x.is_lock_free() << std::endl;
```

atomic 객체가 atomicity하게 구현될 수 있는지를 확인하기 위해

`is_lock_free()` 메서드 호출을 통해 확인할 수 있다.

여기서 *lock free*란, 뮤텍스 같은 객체의 `lock`, `unlock` 없이도 해당 연산을 올바르게 수행할 수 있는지 여부이다.


## memory_order

`atomic` 객체에 원자적 연산 시 어떤 방식으로 메모리에 접근할지 지정할 수 있다.

### memory_order_relaxed

가장 느슨한 메모리 접근 조건으로, 메모리에서 읽거나 쓸 때, **다른 메모리 접근과 순서가 바뀌어도 무방할 때 사용**하는 조건

#### example

```cpp
#include <atomic>
#include <cstdio>
#include <thread>
#include <vector>

void t1(std::atomic<int>* a, std::atomic<int>* b) {
  b->store(1, std::memory_order_relaxed);      // b = 1 (쓰기)
  int x = a->load(std::memory_order_relaxed);  // x = a (읽기)

  printf("x : %d\n", x);
}

void t2(std::atomic<int>* a, std::atomic<int>* b) {
  a->store(1, std::memory_order_relaxed);      // a = 1 (쓰기)
  int y = b->load(std::memory_order_relaxed);  // y = b (읽기)

  printf("y : %d\n", y);
}

void test_memory_order_relaxed() {
  std::vector<std::thread> threads;

  std::atomic<int> a(0);
  std::atomic<int> b(0);

  threads.push_back(std::thread(t1, &a, &b));
  threads.push_back(std::thread(t2, &a, &b));

  for (int i = 0; i < threads.size(); i++) {
    threads[i].join();
  }
}

int main() {
  // tests
  test_memory_order_relaxed();

  return 0;
}
```

위 예시로 실행 결과는 
```
x : 0
y : 1
```

```
x : 1
y : 0
```

```
x : 1
y : 1
```

중 하나가 출력될 것이다.

`memory_order_relaxed`는 메모리 연산 순서를 느슨하게 가져가기 때문에,
메모리 연산에 대해 CPU가 순서를 재배치할 수 있다.

따라서
```
x : 0
y : 0
```

같은 결과가 가능하다.

연산 순서가 자유롭기 때문에, 예상하지 못한 결과를 가져올 수 있지만

위의 `counter` 변수를 증가시키는 예시에서는 `memory_order_relaxed`로 연산해도 결과값이 동일하다.

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>
using std::memory_order_relaxed;

void worker(std::atomic<int>* counter) {
  for (int i = 0; i < 10000; i++) {
    // 다른 연산들 수행

    counter->fetch_add(1, memory_order_relaxed);
  }
}
int main() {
  std::vector<std::thread> threads;

  std::atomic<int> counter(0);

  for (int i = 0; i < 4; i++) {
    threads.push_back(std::thread(worker, &counter));
  }

  for (int i = 0; i < 4; i++) {
    threads[i].join();
  }

  std::cout << "Counter : " << counter << std::endl;
}
```

`counter++` 연산의 atomicity만 보장이 된다면 어떤 시점에 증가하던지 전혀 상관이 없다.


하지만 producer-consumer 문제의 경우 `memory_order_relaxed`의 자유로움으로 인해 원하지 않는 결과를 얻을 수 있다.

```cpp
#include <atomic>
#include <cstdio>
#include <thread>
#include <vector>

void producer(std::atomic<bool>* is_ready, int* data) {
  *data = 10;
  is_ready->store(true, std::memory_order_relaxed);
}

void consumer(std::atomic<bool>* is_ready, int* data) {
  while (!is_ready->load(std::memory_order_relaxed));

  printf("Data : %d\n", *data);
}

int main() {
  std::vector<std::thread> threads;

  std::atomic<bool> is_ready(false);
  int data = 0;

  threads.push_back(std::thread(producer, &is_ready, &data));
  threads.push_back(std::thread(consumer, &is_ready, &data));

  for (int i = 0; i < threads.size(); i++) {
    threads[i].join();
  }

  return 0;
}
```

`producer` 스레드 함수에서 `*data = 10`과 `is_ready->store()` 연산의 순서가 바뀌어 실행된다면 consumer는 변경되지 않은 data `0`을 읽을 수 있다.

위 같은 코드에서는 `memory_order_relaxed`를 사용할 수 없다.

### memory_order_acquire, memory_order_release

#### example

```cpp
#include <atomic>
#include <cstdio>
#include <thread>
#include <vector>

void producer(std::atomic<bool>* is_ready, int* data) {
  *data = 10;
  is_ready->store(true, std::memory_order_release);
}

void consumer(std::atomic<bool>* is_ready, int* data) {
  // data 준비까지 대기
  while (!is_ready->load(std::memory_order_acquire));

  printf("Data : %d\n", *data);
}

int main() {
  std::vector<std::thread> threads;

  std::atomic<bool> is_ready(false);
  int data = 0;

  threads.push_back(std::thread(producer, &is_ready, &data));
  threads.push_back(std::thread(consumer, &is_ready, &data));

  for (int i = 0; i < threads.size(); i++) {
    threads[i].join();
  }

  return 0;
}
```

위 코드에서 `Data : 0` 이 출력되는 것은 불가능하다.

- `memory_order_release`는 이전의 모든 쓰기 연산이 현재 `release` 연산보다 먼저 완료됨을 보장한다. 
	- 같은 변수를 `memory_order_acquire`로 읽는 스레드가 있다면 해당 `release` 연산 전에 발생한 모든 쓰기 작업의 결과를 볼 수 있다.
- `memory_order_acquire`는 이후의 모든 읽기 연산이 현재 `acquire` 연산보다 나중에 완료됨을 보장한다.

**`memory_order_release`와 `acquire`은 짝을 이루어 사용**된다.

### memory_order_acq_rel

`memory_order_acq_rel`은 `acquire`과 `release`를 모두 수행한다.

`fetch_add()`, `fetch_sub()`, `fetch_or()`, `fetch_and()`, `fetch_xor()` 처럼
원자적으로 값을 더하거나 빼는 등의 연산을 수행하고 연산 전의 값을 반환하는,

즉, **읽기 쓰기를 모두 수행하는 명령에서 사용**될 수 있다.

### memory_order_seq_cst

가장 강력한 order로, 모든 스레드에 대해 단일하고 일관된 연산 순서를 보장한다.

모든 스레드에서 모든 시점에 동일한 값을 관찰할 수 있는 만큼 **동기화 오버헤드가 크다**.

`atomic` 객체를 사용할 때 `memory_order`를 명시하지 않으면 자동으로 `memory_order_seq_cst`가 지정된다.

**X86 CPU**의 경우 대부분 **sequential consistency**가 보장되기 때문에 `memory_order_seq_cst`로 강제하여 사용해도 성능 저하가 크지 않지만,

**ARM CPU** 는 동기화 비용이 크기 때문에 꼭 필요할 때만 해당 순서를 사용해야한다.

#### example

```cpp
#include <atomic>
#include <cassert>
#include <thread>

std::atomic<bool> x = {false};
std::atomic<bool> y = {false};
std::atomic<int> z = {0};

void write_x() { x.store(true, std::memory_order_seq_cst); }

void write_y() { y.store(true, std::memory_order_seq_cst); }

void read_x_then_y() {
  while (!x.load(std::memory_order_seq_cst));

  if (y.load(std::memory_order_seq_cst)) ++z;
}

void read_y_then_x() {
  while (!y.load(std::memory_order_seq_cst));

  if (x.load(std::memory_order_seq_cst)) ++z;
}

int main() {
  std::thread a(write_x);
  std::thread b(write_y);
  std::thread c(read_x_then_y);
  std::thread d(read_y_then_x);

  a.join();
  b.join();
  c.join();
  d.join();

  assert(z.load() != 0);  // z값은 최소 1 이상
}
```

위 예시 코드에서 `x`, `y`에 대한 수정을 `c`, `d` 스레드가 관찰할 때, `memory_order_seq_cst` 가 아닌 다른 순서를 사용하면 반대 순서로 관찰할 위험이 있다.

1. `write_x`, `write_y` 스레드가 `x`, `y`를 `true`로 설정
2. `read_x_then_y` 스레드는 `x` 가 `true`가 될때까지 기다린 후 `y`가 `true`인지 확인하고 `z`증가
3. `read_y_then_x` 스레드는 `y` 가 `true`가 될때까지 기다린 후 `x`가 `true`인지 확인하고 `z`증가

`seq_cst` 때문에 `read` 스레드 두개가 `x`, `y`의 변경을 동일한 순서로 관찰하므로
적어도 한 스레드는 조건문을 통과하여 `z`값을 증가시킨다.

## volatile 과의 관계

`volatile`도 `atomic`처럼 컴파일러 최적화로 인한 순서 변경을 제한한다.

`volatile`이 붙은 변수는 컴파일러 최적화 대산에서 제외되어 `volatile` 변수에 접근할 때마다 무조건 메모리에서 값을 읽고, 메모리에 값을 써야 한다.

같은 스레드 내에서는 `volatile` 읽기 쓰기가 다른 코드와 순서가 바뀌지 않지만,
다른 스레드는 그 순서를 보장하지 않는다.

`volatile` 읽기 쓰기 자체가 atomic하지 않기 때문에, **race condition**이 발생할 수 있다.

Visual Studio에서는 volatile 읽기 쓰기가 `release`, `acquire` semantics를 가지기 때문에 스레드 동기화에 사용할 수 있지만 표준은 아님