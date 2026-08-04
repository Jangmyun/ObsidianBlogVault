---
title:
description:
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

