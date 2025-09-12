---
title: Basic Scala Language Elements
description: 스칼라 언어 기초
draft: false
tags:
  - plt
---

## Variables

```scala
// val -> immutable variables
val msg = "Hello, world!"
val b = 3.14
val y: Int = 20 // Int type

// var -> mutable variables
var x: Int = 10
var a = 10
```

## Functions

```scala
def add(x: Int, y: Int): Int = {
	x + y
}
```

 
```scala
def areaOfSquare(a: Int) = a * a

@main def runAreaCalculator(): Unit = {
	println(areaOfSquare(5))
}
```

`@main` 어노테이션은 프로그램의 entry point를 정의함

다른 언어들의 `main` 함수와 동일하게 동작한다고 생각하면 됨

`scala example.scala` 로 인터프리터 실행 가능

## **Type**

```scala
trait typeId
case class variant1(field1: type, ...) extends typeId
case class variant2(field1: type, ...) extends typeId
```

`trait` == type

`trait`은 Java의 interface와 비슷한데, 다중 상속을 지원함

class는 다양한 traits를 상속할 수 있다.

### example

```scala
trait Shape
case class Triangle(a: Int, b: Int, c: Int) extends Shape
case class Rectangle(height: Int, width: Int) extends Shape
case class Square(side: Int) extends Shape
```


## Pattern Matching

Scala의 강력한 기능 중 하나로, 간결한 코드로 가독성을 챙길 수 있다

**exhaustivity checking (완전성 검사)** 와 **reachability checking (도달 가능성 검사)** 를 지원하여 모든 경우의 수를 다뤘는지, 특정 코드에 도달할 수 있는지를 컴파일러가 검사한다.


```scala
// perimeter : Shape => Int
def perimeter(sh: Shape): Int = sh match {
    case Triangle(a, b, c) => a + b + c
    case Rectangle(h, w) => 2 * (h + w)
    case Square(s) => 4 * s
    case _ => -1
}
```

```scala
def interestRate(amount: Double): Double = amount match {
    case x if x <= 1000 => 0.040
    case x if x <= 5000 => 0.045
    case x if x > 5000 => 0.050
}
```


## List

```scala
val x: List[Int] = Nil // List()
val y: List[Int] = List(1,2,3,4)

y.length // 4

42 :: y // 42, 1, 2, 3, 4

y.reverse // List(4,3,2,1)

y.contains(1) // true

y.map(_*2) // List(2,4,6,8)

y.foldLeft(0)(_+_) // List 모든 요소 더하고 0 더하기
y.reduceLeft(0)(_+_) 
```