---
title: "[PLT] Semantics"
description: Semantics(의미론이란 ) 프로그램 실행 중 수행되는 행위를 기술함으로써 프로그램의 의미를 정의하는 방법이다.
draft: false
tags:
  - plt
  - programming_language
---

# Semantics (의미론)
---

## Operational Semantics

> defining the meaning of programs by *describing the actions* carried out during a program's execution
> 프로그램 실행 중 수행되는 *행위를 기술*함으로써 프로그램의 의미를 정의하는 방법

- Natural Semantics (**Big-step**)
	- 프로그램의 시작 상태와 최종 결과만을 정의

### Operational Semantics for What

- Specifying a programming language (프로그래밍 언어 명세)
- Communicating language design ideas 
- Validating claims about languages (언어 검증)
- Validating claims about type systems (타입 시스템 검증)
- Proving correctness of a compiler (컴파일러 정확성 검증)


## Abstract Syntax of Expr

### Inference Rule

$$
\frac{\textit{premise}_1 \quad \textit{premise}_2 \quad \cdots \quad \textit{premise}_n}{\textit{conclusion}}
$$
**Inference rule** 은 horizontal bar로 위아래로 나누어지는데, 의미는 다음과 같다.

$$
\frac{가정}{결론}
$$


### Abstract Syntax of Expr

- 정수 집합:  $n \in Z$
- 규칙
	- $n \in Z \rightarrow n \in A$
	- $e_1 \in A \wedge e_2 \in A \rightarrow e_1 + e_2 \in A$
	- $e_1 \in A \wedge e_2 \in A \rightarrow e_1 - e_2 \in A$

A는 정수와 정수의 덧셈/뺄셈을 포함하는 집합임을 정의

#### BNF style

$$
Z n \quad ::= \quad \cdots \quad |\quad-1\quad|\quad0\quad|\quad1\quad| \quad \cdots
$$
$$
A e \quad::= \quad n \quad| \quad d \quad | \quad e + e \quad| \quad e-e
$$

## Evaluator Semantics of Expr

```scala
// interp : Expr => Int
def interp(expr: Expr): Int = expr match {
	case Num(n) => n
	case Add(l, r) => interp(l) + interp(r)
	case Sub(l, r) => interp(l) - interp(r)
}
```

## Natural Semantics of Expr

$\rightarrow \; \subseteq \; A \times Z$

모든 evaluation relation은 특정 값 ($A \times Z$)의 부분집합이다.

$$
\vdash \; n \rightarrow n
$$
$$
\frac{\vdash \; e_1 \rightarrow n_1 \quad \vdash \; e_2 \rightarrow n_2}
{\vdash \; e_1 + e_2 \rightarrow n_1 + n_2}
$$
$$
\frac{\vdash \; e_1 \rightarrow n_1 \quad \vdash \; e_2 \rightarrow n_2}
{\vdash \; e_1 + e_2 \rightarrow n_1 - n_2}
$$
$4 + (2 - 1) \in A$ 의  증명은 다음과 같다.

![[Pasted image 20250921175221.png]]




| 구분                             | 내용                            |
| ------------------------------ | ----------------------------- |
| **Abstract Syntax (추상 구문)**    | 표현식의 **형태(문법)**를 정의           |
| **BNF 정의**                     | 표현식을 문법적으로 기술                 |
| **Natural Semantics (자연 의미론)** | 표현식이 실제로 어떤 **값으로 평가되는지**를 정의 |
| **Interpreter (실행기 구현)**       | 의미론을 코드로 표현                   |
