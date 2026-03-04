---
title: "[C++] Attributes"
description: "`C++11` 부터 지원되는 기능으로 컴파일러에 추가정보를 전달하거나 코드를 보다 명확하게 만드는 데 사용한다."
draft: false
tags:
  - cpp
---
 
# Attributes


`C++11` 부터 지원되는 기능으로 컴파일러에 추가정보를 전달하거나 코드를 보다 명확하게 만드는 데 사용한다.

## Standard Attributes

### noreturn
#cpp11

함수의 리턴값이 없음을 나타냄.

주로 exception 출력이나 `std::exit`, `std::abort` 의 wrapper 함수에 붙인다.

#### example
```cpp
[[noreturn]] void f() {
	throw "error";
}

void q [[noreturn]] (int i) {
	if (i > 0)
		throw "positive";
}

// void h() [[noreturn]]; // error: 속성은 함수 이름 바로 뒤에 위치해야 함

int main() {
	try { f(); } catch(...) {}
	try { q(42); } catch(...) {}
}
```


### carries_dependency
#cpp11, deprecated in c++26

특정 값이 다른 값에 대한 의존성을 전달한다는 것을 컴파일러에게 알려주는 역할

병렬 프로그래밍의 [[Atomic]] 조작에 있어 값에 의존하는 순서를 함수에 전파

1. 함수 매개변수에 적용하여 함수에 전달된 값이 함수 내부에서 다른 데이터에 대한 의존성임을 전달
```cpp
void process_data(Data* ptr [[carries_dependency]]) {
	// ptr에 의존하는 작업
	// 컴파일러는 carries_dependency로 ptr이 의존성을 전달한다는 것을 알기 때문에
	// 최적화 가능
}
```


2. 함수 리턴값에 적용하여 함수 리턴값이 다른 데이터에 대한 의존성임을 전달
```cpp
[[carries_dependency]] Data* get_data() {
	// data 로드하고 포인터 반환
}
```

멀티스레드에서는 명령의 순서가 매우매우매우 중요한데, CPU가 성능 향상을 위해 명령어 순서를 바꾸는 경우가 있다. 

이걸 막기 위해 **메모리 펜스**를 사용하여 순서 뒤집기를 막아야 하는데, 메모리 펜스는 오버헤드가 있다.

#### 쉬운 설명

스레드 A가 `x` 데이터를 준비해두고 `ptr` 포인터에 넣었고,
스레드 B가 `ptr`을 읽어와서 그 안의 `x` 데이터를 사용한다.

이때, B가 `ptr`만 읽고 `x`를 보려고 하는 순간 CPU가 최적화를 해 순서가 꼬이면
`ptr`을 읽어왔음에도 `x`는 준비되지 않은 상태일 수 있다.

이럴 때 보통 혹시 모르니 메모리 펜스를 위해 멈추게 되는데, 이게 성능 하락의 요인이다.

**\[\[carries_dependency\]\]** 를 붙이면 `ptr`이 데이터 `x`와 연결되어 있기 때문에 순서가 꼬이면 안되지만, 메모리 펜스는 필요없음을 명시하는 것이다.


### deprecated
#cpp14

해당 개체가 더 이상 사용되지 않거나, 새로운 버전으로 대체되었음을 알린다.

```cpp
[[deprecated("This function is outdated. Use new_print() instead.")]]
void old_print() {}

void new_print() {}
```

### fallthrough
#cpp17

`switch` 문에서 `case`블록 끝에 사용해서 의도적으로 다음 `case`로 제어 흐름을 넘기겠다는 것을 컴파일러에 명시

```cpp
void handle_error(int errer_code) {
	switch (error_code) {
		case 1:
			std::cout << "Minor error" << std::endl;
			[[fallthrough]] // 의도적으로 다음 case로 넘김
		case 2:
			std::cout << "Handling critical" << std::endl;
			break;
		default:
			break;
	}
}
```

### maybe_unused
#cpp17

사용되지 않거나 디버그 목적으로만 사용되는 함수, 변수, 매개변수 등에 대해 명시하여 컴파일러 경고를 내지 않도록 함

```cpp
#include <cassert>
 
[[maybe_unused]] void f([[maybe_unused]] bool thing1,
                        [[maybe_unused]] bool thing2)
{
    [[maybe_unused]] lbl: // the label “lbl” is not used, no warning
    [[maybe_unused]] bool b = not false and not true;
    assert(b); // 릴리즈 모드에서는  assert가 컴파일 단계에서 제거되어 b 사용x
} // parameters “thing1” and “thing2” are not used, no warning
 
int main() {}
```


### nodiscard
#cpp17 , \[\[nodiscard("reason")\]\]은 #cpp20

함수나 enum의 리턴값을 반드시 사용해야 함을 알려준다.

```cpp
#include <iostream>

[[nodiscard]] bool is_ok() {
	return true;
}

int main() {
	is_ok(); // 경고 발생
	if (is_ok()) {
		// 반환값을 조건문에 사용
	}
	return 0;
}
```

클래스나 열거형 선언 앞에 붙이면 해당 타입 객체를 반환하는 모든 함수에 `nodiscard`를 적용할 수 있다.

```cpp
[[nodiscard]] enum class ErrorCode {
	OK = 0,
	ERROR = 1
};

ErrorCode get_status() {
	return ErrorCode::OK;
}

int main() {
	get_status(); // 경고 발생
	
	ErrorCode status = get_status(); // ok

	return 0;
}
```


### likely, unlikely
#cpp20

주로 `if-else`문에서 어떤 branch가 더 자주 실행될 것인지 컴파일러에게 힌트를 줘서 명령어 재정렬을 통해 성능 향상을 꾀할 수 있는 착한 친구

```cpp
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>
 
namespace with_attributes
{
    constexpr double pow(double x, long long n) noexcept
    {
        if (n > 0) [[likely]]
            return x * pow(x, n - 1);
        else [[unlikely]]
            return 1;
    }
    constexpr long long fact(long long n) noexcept
    {
        if (n > 1) [[likely]]
            return n * fact(n - 1);
        else [[unlikely]]
            return 1;
    }
    constexpr double cos(double x) noexcept
    {
        constexpr long long precision{16LL};
        double y{};
        for (auto n{0LL}; n < precision; n += 2LL) [[likely]]
            y += pow(x, n) / (n & 2LL ? -fact(n) : fact(n));
        return y;
    }
} // namespace with_attributes
 
namespace no_attributes
{
    constexpr double pow(double x, long long n) noexcept
    {
        if (n > 0)
            return x * pow(x, n - 1);
        else
            return 1;
    }
    constexpr long long fact(long long n) noexcept
    {
        if (n > 1)
            return n * fact(n - 1);
        else
            return 1;
    }
    constexpr double cos(double x) noexcept
    {
        constexpr long long precision{16LL};
        double y{};
        for (auto n{0LL}; n < precision; n += 2LL)
            y += pow(x, n) / (n & 2LL ? -fact(n) : fact(n));
        return y;
    }
} // namespace no_attributes
 
double gen_random() noexcept
{
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static std::uniform_real_distribution<double> dis(-1.0, 1.0);
    return dis(gen);
}
 
volatile double sink{}; // ensures a side effect
 
int main()
{
    for (const auto x : {0.125, 0.25, 0.5, 1. / (1 << 26)})
        std::cout
            << std::setprecision(53)
            << "x = " << x << '\n'
            << std::cos(x) << '\n'
            << with_attributes::cos(x) << '\n'
            << (std::cos(x) == with_attributes::cos(x) ? "equal" : "differ") << '\n';
 
    auto benchmark = [](auto fun, auto rem)
    {
        const auto start = std::chrono::high_resolution_clock::now();
        for (auto size{1ULL}; size != 10'000'000ULL; ++size)
            sink = fun(gen_random());
        const std::chrono::duration<double> diff =
            std::chrono::high_resolution_clock::now() - start;
        std::cout << "Time: " << std::fixed << std::setprecision(6) << diff.count()
                  << " sec " << rem << std::endl; 
    };
 
    benchmark(with_attributes::cos, "(with attributes)");
    benchmark(no_attributes::cos, "(without attributes)");
    benchmark([](double t) { return std::cos(t); }, "(std::cos)");
}
```

위 프로그램을 M1 맥북에서 실행하면 실제로는 

```
x = 0.125
0.99219766722932900560039115589461289346218109130859375
0.99219766722932900560039115589461289346218109130859375
equal
x = 0.25
0.96891242171064473343022882545483298599720001220703125
0.96891242171064473343022882545483298599720001220703125
equal
x = 0.5
0.8775825618903727587394314468838274478912353515625
0.8775825618903727587394314468838274478912353515625
equal
x = 1.490116119384765625e-08
0.99999999999999988897769753748434595763683319091796875
0.99999999999999988897769753748434595763683319091796875
equal
Time: 3.889727 sec (with attributes)
Time: 3.886019 sec (without attributes)
Time: 0.510554 sec (std::cos)
```

차이가 없는 수준이다.

최신 컴파일러는 정적 분석, 프로파일 기반 최적화 (PGO) 등을 사용하여 힌트 없이도 최적화가 가능하고, 
M1 칩의 **Conditional Branch Predictor**가 분기 예측 실패를 빠르게 복구할 수 있다.



### no_unique_address
#cpp20

빈 클래스 (Empty Class)를 구조체나 클래스의 멤버변수로 넣었을 때 불필요한 메모리 공간을 소비하지 않도록 한다.

```cpp
#include <iostream>

class EmptyClass {};

class TestClass {
 public:
  [[no_unique_address]] EmptyClass e;
  int data;
};

int main() {
  TestClass tc;
  std::cout << "TestClass size : " << sizeof(TestClass) << std::endl;
  std::cout << &tc.e << std::endl;
  std::cout << &tc.data << std::endl;
}
```

실행결과는 다음과 같다. (환경에 따라 다를 수 있다.)

```
TestClass size : 4
0x16d95aaac
0x16d95aaac
```

\[\[no_unique_address\]\]를 사용하지 않으면 빈 객체 또한 고유한 주소를 가져야하므로 결과는 다음과 같다.

```
TestClass size : 8
0x16b24aaa8
0x16b24aaac
```


이외에도 

### assume

### indeterminate

### optimize_for_synchronized

등이 있는데, c++20 이후 기능은 아직 다루지 않도록 함 (20도 아직 제대로 못쓰고 있다...)