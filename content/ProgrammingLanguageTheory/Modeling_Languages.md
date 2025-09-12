---
title: "[PLT] Modeling Languages"
description: Example Description
draft: true
tags:
  - plt
---
 
![[Screenshot 2025-09-12 at 21.08.03.png]]

### Interpreter vs. Compiler
#### Interpreter

source code를 바로 실행하는 프로그램

#### Compiler

source code를 다른 언어로 변환하는 프로그램


## Syntax & Semantics

### Syntax

모든 언어는
- 고유한 문법
- 각 문법과 연관된 동작
- 여러 유용한 라이브러리
- 해당 언어의 프로그래머들이 사용하는 idioms (관용구) 모음

#### Concrete Syntax

- `3 + 4`: infix
- `3 4 +`: postfix
- `+ 3 4`: prefix
- `{+ 3 4}`: parenthesized prefix

#### Abstract Syntax

![[Screenshot 2025-09-12 at 21.18.47.png]]

### Semantics (의미론)

- Mathmatical Techniques
	- [Denotational Semantics](https://en.wikipedia.org/wiki/Denotational_semantics)
	- [Operational Semantics](https://en.wikipedia.org/wiki/Operational_semantics)
	- [Axiomatic Semantics](https://en.wikipedia.org/wiki/Axiomatic_semantics)
- Interpreter Semantics
	- interpreter를 설명하기 위해 인터프리터를 작성


### Programming Language

프로그래밍 언어는 

- a grammar for programs
- rules for evaluating any program to produce a result

에 의해 정의된다.


## A Grammar for Arithmetic Expressions

### **BNF** (Backus-Naur Form)

 ![[Screenshot 2025-09-12 at 21.28.46.png]]

- **`expr`: Non-terminal** - 문법 규칙에  따라 다른 형태로 바뀔 수 있는
- **`::=`**: 왼쪽의 non-terminal 기호가 오른쪽 규칙으로 정의될 수 있음
- **|** : "or"
- **Terminal**: `{`, `+`, `-`, `}` 처럼 따옴표로 묶인 literal -> 문법 규칙에서 변경될 수 없는 부분
- **Literal**: 문법에 명시적으로 지정된 `""` 로 묶인 고정값

```
{+ 34 20}
{+ {- 4 3} 40}
```

`{ - expr expr}` 또한 `expr`이므로 `{+ {- 4 3} 40}` 도 가능하다

```bnf
expr ::= "{" "+" num num "}"
		| "{" "-" num num "}"
		| num
```

위처럼 addition, subtraction 연산의 피연산자로 num을 사용해도 괜찮을까?

위 BNF 문법을 사용해서 `{+ {- 4 3} 56}` 같은 수를 인식할 수는 없다.

`+`와 `-` 연산 시 항상 `num` 만을 받기 때문에 연산의 중첩이 허용되지 않는다.

```bnf
expr ::= "{" "+" expr expr "}"
		| "{" "-" expr expr "}"
		| num
```

위 식을 Scala 언어로 구현해보면 다음과 같다

```scala
trait Expr
case class Num(num: Int) extends Expr
case class Add(left: Expr, right: Expr) extends Expr
case class Sub(left: Expr, right: Expr) extends Expr
```

```scala
val expr = Add(Num(3), Sub(Num(8), Num(2)))
expr.left // type: Expr, value: Num(3)
```

BNF로 구현한 addition expr과 subtraction expr을 스칼라로 표현하면 위와 같다.
#### Additional BNF notations

```bnf
<statement> ::= <variable_declaration> ";" | <assignment> ";"
<variable_declaration> ::= "var" <identifier> [ "=" <expression> ]
<assignment> ::= <identifier> "=" <expression>
<expression> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= <number> | "(" <expression> ")"
<number> ::= <digit>+
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<identifier> ::= <letter> { <letter> | <digit> }
<letter> ::= "a" | "b" | "c" | ... | "z" | "A" | "B" | "C" | ... | "Z"
```

- `<>` 꺾쇠로 묶인 것은 **non-terminal**이다. 규칙에 따라 다른 형태로 바뀔 수 있다.
- `::=`: 왼쪽의 non-terminal 기호가 오른쪽 규칙으로 만들어질 수 있다
- `"..."` 따옴표로 묶인 것은 **terminal**기호이므로 더 이상 나눌 수 없는 기호이다.
- `[]` 대괄호로 묶인 것은 **선택적**이라는 뜻으로, 있어도 되고 없어도 된다.
- `{}` 중괄호로 묶인 것은 **0번 이상 반복될 수 있다**는 뜻이다.
- `()` 괄호로 묶인 것은 **grouping**이다.
- `+`: 하나 이상
- `?`: optional
- `*`: 0 이상


#### BNF 예시

- [Java BNF](https://users-cs.au.dk/amoeller/RegAut/JavaBNF.html)
- [C BNF](https://cs.wmich.edu/~gupta/teaching/cs4850/sumII06/The%20syntax%20of%20C%20in%20Backus-Naur%20form.htm)
