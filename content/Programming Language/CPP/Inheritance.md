---
title: "[C++] Inheritance (상속)"
description: 상속, virtual 오버라이딩, 업/다운캐스팅, 다중 상속까지 다루는 C++ 상속 정리 노트.
draft: false
tags:
  - cpp
---
# Inheritance (상속)

상속은 보통 **is-a** 관계로 설명되는데, 여러가지 탈 것 객체를 만들어야 한다고 생각했을 때, 자동차, 비행기, 배 모두 '탈 것' 이므로 '탈 것' 객체를 먼저 만들고 이를 상속받는 자동차, 비행기, 배 객체를 만드는 것이 하나의 예시이다.

```cpp
class Vehicle 
{
public:
	void ride();
}

class Car : public Vehicle 
{
public:
	void sideMirror(); // 대충 지음
}
```

여기서 `Car` 는 `Vehicle` 이 가진 특성 (예시에서는 `ride()`) 을 그대로 물려받는다.

`Car` 입장에서는 `Vehicle` 과의 관계가 명확하지만, `Vehicle`이 정의되는 시점에는 `Car`의 존재를 알 수 없다. 따라서 `Vehicle`는 `Car` 의 메서드나 멤버를 사용할 수 없다.

어떤 객체를 포인터/레퍼런스로 가리킬 때, 그 객체 클래스의 파생 클래스 객체도 가리킬 수 있다.

```cpp
Vehicle* v = new Car();
```

위 처럼 작성하면 타입이 안맞지만 정상적으로 컴파일된다.
하지만 위 `Vehicle* v` 포인터로 `Car` 클래스의 메서드를 호출할 수는 없다.

자식 클래스는 부모 클래스에 선언된 `public`/`protected` 메서드나 데이터 멤버를 자신의 클래스 안에서 정의한 것처럼 사용할 수 있다.

#### 접근 제어 지정자

| 접근자         | 접근 가능 범위         | 용도                        |
| ----------- | ---------------- | ------------------------- |
| `public`    | 어디서나             | 클라이언트용 메서드, getter/setter |
| `protected` | 같은 클래스 + 파생 클래스  | 외부에 감출 헬퍼 메서드             |
| `private`   | 같은 클래스만 (파생 불가능) | 데이터 멤버 기본값, 내부 구현 전용      |

### 상속 방지

클래스 정의할 때 `final` 키워드를 붙이면 다른 클래스가 해당 클래스를 상속할 수 없게 된다.

```cpp
// 객체 상속 방지
class Base final {};
```

## 메서드 오버라이딩

Base 클래스에서 받은 메서드를 파생 클래스에서 재정의하는 것을 **오버라이딩** 이라고 한다.

C++에서는 `virtual` 키워드를 가진 메서드만 오버라이드 할 수 있다.

```cpp
class Base
{
public:
	virtual void someMethod();
protected:
	int mProtectedInt;
private:
	int mPrivateInt;
}
```

`virtual` 키워드는 소멸자에는 사용 가능하지만 소멸자에는 사용 불가능하다.

보통 상속해도 되는 클래스의 경우 모든 메서드를 `virtual` 로 선언하는데, 성능이 떨어지는 문제점이 있다.

메서드를 오버라이딩 하는 문법은 아래와 같다:

```cpp
class Derived : public Base
{
public:
	virtual void someMethod() override; // Base의 someMethod() 오버라이딩
}
```

`override` 키워드는 필수는 아니나 명시적으로 적는 것이 좋다.
마찬가지로 파생 클래스에 `virtual` 키워드가 이 없어도 base 클래스에서 virtual 로 정의하면 virtual 상태를 유지한다.


포인터나 레퍼런스는 해당 클래스의 파생 클래스 객체까지 가리킬 수 있다고 앞에서 얘기했다.
이때, 객체는 virtual 메서드를 호출할 때 가장 적절한 메서드를 호출한다.

```cpp
Derived myD;
Base& ref = myD;
ref.someMethod(); // Derived의 someMethod() 가 호출
```

베이스 클래스에 정의되지 않은 파생 클래스의 데이터 멤버나 메서드에는 접근할 수 없다.

```cpp
Derived myD;
Base& ref = myD;
myD.someOtherMethod(); // 정상
ref.someOtherMethod(); // 에러
```

파생 클래스를 베이스 클래스로 타입 캐스팅하게 되면 메모리 영역이 축소되면서 파생 클래스에 추가한 정보가 사라진다.

### override 키워드를 붙이는 이유

`override` 키워드는 필수가 아니다. 그럼에도 필요한 이유가 있다:

```cpp
class Base {
public:
	virtual void someMethod(double d);
}

class Derived : public Base{
public:
	virtual void someMethod(int i); // !! 실수로 함수 시그니처를 다르게 오버라이드 한 경우
}

// ...

Derived myD;
Base& ref = myD;
ref.someMethod(1.0); // Derived 가 아니라 Base의 someMethod()가 호출됨
```

위는 오버라이딩 시 실수로 함수 시그니처를 다르게 작성한 경우이다.
이런 경우 오버라이딩한 함수가 아니라 Base 클래스의 메서드가 실행되게 되지만, override 키워드를 빼먹었으니 명시적으로 알 수가 없다.

`override` 키워드를 붙이게 되면 컴파일 시 일치하는 함수 시그니처가 없으면 바로 에러로 알 수 있으니 무조건 쓰는게 좋다고 볼 수 있다.

### virtual 과 vtable

Base 클래스에서 `virtual` 이 없는 메서드를 Derived 클래스에서 재정의하는 것은 오버라이드가 아니라 **숨기기 (hiding)** 가 된다.

```cpp
lass Base {
public:
    void go() { cout << "go() called on Base" << endl; }
};

class Derived : public Base {
public:
    void go() { cout << "go() called on Derived" << endl; }
};

Derived myDerived;
Base& ref { myDerived };
ref.go(); // "go() called on Base" 출력
```

위 예시에서 `Derived` 객체로 직접 호출 시에는 `Derived` 에서 정의한 `go()` 가 실행되지만 `Base`참조를 통해 호출하면 `Base` 의 메서드가 호출된다.

이때 `Derived::go()` 와 `Base::go()` 는 오버라이드된 메서드가 아니라 완전히 별개의 메서드로 취급된다.

`virtual`로 선언한 메서드는 실행 시점 (Runtime) 에 객체의 실제 타입에 맞춰 적절한 함수를 호출한다. 이를 **동적 바인딩 (dynamic binding)** 이라고 한다.

가상함수가 존재하는 클래스는 **vtable** 이 생성되는데, 이 테이블에 클래스에 정의된 `virtual` 함수들의 주소값을 담고, 해당 클래스의 모든 객체들은 내부적으로 **vtable 포인터**를 가지게 된다.

메서드의 오버라이드를 막으려면 [[#상속 방지]] 방법과 마찬가지로 `final` 키워드를 붙이면 된다.

```cpp
class Base {
public:
    virtual ~Base() = default;
    virtual void someMethod();
};

class Derived : public Base {
public:
    void someMethod() override final;  // Preventing Overriding
};

class DerivedDerived : public Derived {
public:
    void someMethod() override; // 컴파일 에러!
};
```

### 부모 생성자와 소멸자의 호출 순서

#### 생성자 (constructor)

어떤 클래스를 상속하는 클래스의 객체는 부모와 함께 실행된다.

1. Base 클래스가 존재하면 **Base의 기본 생성자**가 먼저 실행
	- 단 **ctor 이니셜라이저** ([[Member_Initializer_List]]) 를 통해 Base 의 생성자를 먼저 호출했으면 해당 생성자가 대신 호출됨
2. **non-static** 데이터 멤버들이 선언 순서대로 생성
3. 클래스 **자신의 생성자** 본문 실행

#### 소멸자 (destructor)

**‼️소멸자는 반드시 `virtual` 로 선언해야 한다‼️** (클래스를 `final` 로 설정하지 않은 이상)

컴파일러가 자동 생성하는 기본 소멸자는 `virtual` 이 아니라서 베이스 클래스에서 소멸자를 명시적으로 정의하거나 `=virtual` 로 소멸자를 선언해야 한다.

소멸 순서는 생성자와 반대이다.

1. **자신 클래스의 소멸자** 본문 실행
2. 클래스의 **데이터 멤버들의 생성의 역순**으로 소멸
3. **부모 클래스** 소멸

### 부모 버전 메서드 호출

오버라이드 한 메서드에서 부모 동작에 추가 기능을 붙이고 싶으면 아래처럼 범위 지정 연산자 `::` 를 사용하면 된다.

```cpp
string MyWeatherPrediction::getTemperature() const 
{
    return WeatherPrediction::getTemperature() + "\u00B0F";
}
```

### 업캐스팅과 다운캐스팅

Base 클래스 타입으로 Derived 클래스를 참조하는 것을 **업캐스팅 (upcasting)** 이라고 한다.
반대로 Base 클래스를 Derived 클래스로 캐스팅하는 것을 **다운캐스팅 (downcasting)** 이라고 한다.

#### 업캐스팅 (upcasting)

업캐스팅 시 Derived 클래스를 통째로 베이스 클래스 객체에 대입하면 **슬라이싱**이 발생한다.

**포인터나 참조**를 이용해 받으면 슬라이싱이 일어나지 않는다.

```cpp
Base myBase { myDerived }; // Slicing 발생

Base& myBase { myDerived }; // No Slicing
```

#### 다운캐스팅 (downcasting)

다운캐스팅은 일반적으로 지양해야한다.

```cpp
void presumptuous(Base* base)
{
    Derived* myDerived { static_cast<Derived*>(base) };
    // Derived 메서드 사용...
}
```

위 예시에서 `presumptuous()` 를 호출하는 다른 프로그래머가 `Derived` 가 아니라 `Base` 를 넘기면 컴파일 시간에 인수의 타입을 결정할 수 없다.

다운캐스팅이 불가피할 때는 `dynamic_cast()` 를 사용한다.
이 함수는 객체 내부에 vtable을 확인해서 캐스팅이 잘못된 경우에 처리하지 않는다.

```cpp
void lessPresumptuous(Base* base) 
{
    Derived* myDerived { dynamic_cast<Derived*>(base) };
    if (myDerived != nullptr) {
        // 안전하게 Derived 메서드 사용
    }
}
```

`dynamic_cast()` 가 실패한 경우
- 포인트: `nullptr` 반환
- 레퍼런스: `std:bad_cast` 익셉션 발생
한다.

다운캐스팅 자체를 지양하고 **다형성**을 활용하도록 바꾸는 것이 좋다.

## 다형성을 위한 상속

**전문가를 위한 C++** 책에서는 SpreadsheetCell 클래스를 활용한 다형성 예시를 보여준다.

```cpp
class SpreadsheetCell
{
public:
    virtual ~SpreadsheetCell() = default;
    virtual void set(std::string_view value);
    virtual std::string getString() const;
};
```

Base 클래스인 `SpreadsheetCell` 에서 이 클래스를 상속받을 공통 동작을 정의해야 하는데, Base 클래스에 데이터 멤버가 없이 이를 활용하는 동작을 선언하려면 Base 클래스를 추상 클래스로 만드는 방법이 있다.

### 순수 가상 메서드 (pure virtual method) 와 추상 클래스 (abstract class)

**순수 가상 메서드 (pure virtual method)** 는 클래스를 정의할 때 명시적으로 정의하지 않는 메서드이다.

순수 가상 메서드를 지정하려면 메서드 선언 뒤에 `= 0` 을 붙이고 메서드를 구현하는 코드를 작성하지 않는다.

순수 가상 메서드가 하나라도 포함된 클래스는 **추상 클래스**가 되고, 인스턴스를 생성할 수 없게 된다.

```cpp
class SpreadsheetCell
{
public:
    virtual ~SpreadsheetCell() = default;
    virtual void set(std::string_view value) = 0; // 순수 가상 메서드
    virtual std::string getString() const = 0; // 순수 가상 메서드
};

SpreadsheetCell cell; // 컴파일 에러 발생 !
```

추상 클래스를 정의할 때 메서드는 대부분 순수 가상 메서드로, 소멸자는 명시적으로 `default` 로 선언한다.

### 파생 클래스 구현

#### StringSpreadsheetCell 클래스 정의 및 구현

```cpp
class StringSpreadsheetCell : public SpreadsheetCell
{
public:
	virtual void set(std::string_view inString) override;
	virtual std::string getString() const override;
	
private:
	std::optional<std::string> mValue; 
}

void StringSpreadsheetCell::set(string_view inString) {
	mValue = inString;
}

string StringSpreadsheetCell::getString() const {
	return mValue.value_or("");
}
```

`optional<string>`([[Optional]]) 을 사용해 `string` 타입 셀에 값이 설정 됐는지 쉽게 확인할 수 있도록 한다.

##### DoubleSpreadsheetCell 구현

```cpp
class DoubleSpreadsheetCell : public SpreadsheetCell
{
public:
	virtual void set(double inDouble) override;
	virtual void set(std::string_view inString) override;
	virtual std::string getString() const override;
	
private:
	static std::string doubleToString(double inValue);
	static double stringToDouble(std::string_view inValue);
	
	std::optional<double> mValue;
}

void DoubleSpreadsheetCell::set(double inDouble){
	mValue = inDouble;
}

void DoubleSpreadsheetCell::set(string_view inString){
	mValue = stringToDouble(inString);
}

std::string DoubleSpreadsheetCell::getString() const {
	return (mValue.has_value() ? doubleToString(mValue.value()) : "");
}
```

`DoubleSpreadsheetCell` 클래스의 경우 `double`을 인수로 받는 `set()` 을 별도로 정의한다.

위처럼 클래스를 계층화하면 다형성의 장점을 활용할 수 있다.

```cpp
vector<unique_ptr<SpreadsheetCell>> cellArray;

cellArray.push_back(make_unique<StringSpreadsheetCell>());
cellArray.push_back(make_unique<StringSpreadsheetCell>());
cellArray.push_back(make_unique<DoubleSpreadsheetCell>());

cellArray[0]->set("hello");
cellArray[1]->set("10");
cellArray[2]->set("5.5");
```

`vector` 에 서로 다른 데이터를 저장할 수 있게 되고, `SpreadsheetCell` 에 정의한 메서드를 내부 구현을 몰라도 호출하여 사용할 수 있다.

### 형제 (Peer) 클래스 간 변환 - 변환 생성자 (Converting Constructor)

**변환 생성자 (converting constructor / typed  constructor)** 를 사용해 같은 Base 클래스를 상속받는 Peer (형제) 클래스 간 타입을 변환할 수 있다.

```cpp
export class StringSpreadsheetCell : public SpreadsheetCell
{
public:
    StringSpreadsheetCell() = default;
    StringSpreadsheetCell(const DoubleSpreadsheetCell& cell);
    
    // 구현을 내부에서 깔끔하게 끝내고 싶다면
    // StringSpreadsheetCell(const DoubleSpreadsheetCell& cell)
    //    : m_value { cell.getString() }
    //{ }
    
    // 나머지 생략
};

StringSpreadsheetCell::StringSpreadsheetCell(
	const DoubleSpreadsheetCell& cell)
{
	mValue = cell.getString();
}
```

**‼️생성자를 하나라도 직접 선언하면 기본 생성자가 자동으로 생성되지 않는다**
따라서 `StringSpreadsheetCell() = default` 로 기본 생성자를 명시적으로 선언해야 한다.

## 다중 상속 (Multiple Inheritance)

여러 클래스를 한번에 상속받을 수도 있다.

```cpp
class Baz : public Foo, public Bar
{
};
```

- `Foo`, `Bar` 양쪽의 `public` 메서드와 데이터 멤버를 지원
- `Baz` 의 메서드는 `Foo`, `Bar` 양쪽의 `protected` 멤버에 접근 가능
- `Foo`, `Bar` 어느 쪽으로도 업캐스트 가능
- 생성 시 **부모 선언 순서**대로 기본 생성자 호출
- 소멸 시 선언의 역순으로 소멸자 호출

### 모호한 이름 (Name Ambiguity)

```cpp
class Dog {
public:
	virtual void eat() { cout << "The dog ate." << endl; }
    virtual void bark() { cout << "Woof!" << endl; }
};

class Bird {
public:
	virtual void eat() { cout << "The bird ate." << endl; }
    virtual void chirp() { cout << "Chirp!" << endl; }
};

class DogBird : public Dog, public Bird
{
};

int main() {
	DogBird myDB;
	myDB.eat(); // 에러!
	return 0;
}
```

위는 상속받는 두 클래스에 이름이 같은 `eat()` 메서드가 존재하는 경우이다. 클라이언트가 `eat()` 을 호출하지 않으면 문제가 발생하지 않지만 호출하는 코드를 작성하고 컴파일하면 에러를 발생한다.

모호한 상황을 피하려면

1. `dynamic_cast` 로 명시적 업캐스트
	- `dynamic_cast<Dog&>(myDB).eat();`
2. 범위 지정 연산자로 직접 명시
	- `myDB.Dog::eat();`
3. 해당 클래스 자체에서 어느 버전을 쓸지 정의
	- `void eat() override { Dog::eat(); }`

### 모호한 베이스 클래스 (Ambiguous Base Classes)

같은 클래스를 두 번 상속할 때도 모호한 상황이 발생한다.

```cpp
class Dog {};
class Bird : public Dog {};
class DogBird : public Bird, public Dog {}; // 에러!
```

또는 아래처럼 부모가 겹치는 형태가 있을 수 있다.

```cpp
class Animal
{
public:
    void sleep() { cout << "Zzz..." << endl; }
};

class Dog : public Animal
{
public:
    void bark() { cout << "Woof!" << endl; }
};

class Bird : public Animal
{
public:
    void chirp() { cout << "Chirp!" << endl; }
};

class DogBird : public Dog, public Bird
{
};

int main()
{
    DogBird myConfusedAnimal;
    myConfusedAnimal.bark();   // OK
    myConfusedAnimal.chirp();  // OK
    myConfusedAnimal.sleep();  // 에러! 모호함 (Dog::Animal::sleep()? Bird::Animal::sleep()?)
}
```

클래스 계층이 위처럼 다이아몬드 형태 (한 클래스를 상속받는 두 클래스를 상속) 일 때, 최상위 클래스를 **순수 가상 메서드** ([[#순수 가상 메서드 (pure virtual method) 와 추상 클래스 (abstract class)]]) 로 만들어서 호출할 메서드를 없애면 된다.

