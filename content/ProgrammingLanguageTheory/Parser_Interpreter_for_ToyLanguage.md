---
title: "[PLT] Parser and Interpreter for ToyLang"
description: Example Description
draft: true
tags:
  - plt
  - programming_language
---
이전 강의 ([[Modeling_Languages]]) 에서 Scala를 사용해서 간단한 `Expr`을 구현했다.

```scala
trait Expr
case class Num(num: Int) extends Expr
case class Add(left: Expr, right: Expr) extends Expr
case class Sub(left: Expr, right: Expr) extends Expr
```

#### An interpreter function for AE

```scala
// trait Expr ...

// [Contract] interp : Expr => Int
def interp(expr: Expr): Int = expr match {
	case Num(n) => n
	case Add(l, r) => interp(l) + interp(r)
	case Sub(l, r) => interp(l) + interp(r)
}

@main def run(): Unit = {
	val expr = Add(Num(3), Sub(Num(8), Num(2))) // "{+ 3 {- 8 2}}"
	println(interp(expr)) // 9
}
```

## Parser

파서는 컴파일러나 인터프리터의 핵심 컴포넌트로,

- 입력된 program(code) 이 어떤 종류의 문장이나 표현인지 분석하고
- **Concrete syntax**를 **Abstract syntax**로 변환한다.

**BNF**를 통해 **Concrete Syntax**를 정의할 수 있다.



![[Screenshot 2025-09-13 at 00.43.51.png]]

Concrete Syntax가 달라도 같은 Abstract syntax로 변환될 수도 있다.

**Abstract Syntax**는 트리 구조와도 비슷하기 때문에 **Abstract Syntax Tree (AST)** 라고도 불린다. ('`Add(Num(4), Num(2))`')

### Parser for Arithmetic Expression

```scala
def parse(input: String): Expr = {
  object Parser extends RegexParsers {
    def int: Parser[Int] = """\d+""".r ^^ { _.toInt }
    def wrap[T](parser: Parser[T]): Parser[T] = "{" ~> parser <~ "}"
    lazy val expr: Parser[Expr] =
      int ^^ { case n => Num(n) } |
        wrap("+" ~> expr ~ expr) ^^ { case l ~ r => Add(l, r) } |
        wrap("-" ~> expr ~ expr) ^^ { case l ~ r => Sub(l, r) }
    def parseAllExpr(input: String): Expr =
      parseAll(expr, input).getOrElse(
        throw new SimpleException(s"bad syntax: $input")
      )
  }
  Parser.parseAllExpr(input)
}

// Custom exception for this class
class SimpleException(message: String) extends RuntimeException(message) {
  override def fillInStackTrace(): Throwable = this
  override def printStackTrace(): Unit = println(message)
}
```

위 파서를 사용하여 아래 구문들을 파싱하면

```ae
parse("3")
parse("{+ 3 4}")
parse("{+ {- 3 4} 7}")
parse("{- 5 1 2}")
```

```abstract
Num(3)
Add(Num(3),Num(4))
Add(Sub(Num(3),Num(4)),Num(7))
Sub(Num(5), Num(1), Num(2)) ???
```

위 처럼 Abstract syntax로 변환될 것이다.

### BIg Picture (modeling languages)

![[Screenshot 2025-09-13 at 01.14.10.png]]

parser는 concrete를 abstract syntax로 변환하고, 인터프리터는 abstract syntax를 interpret(해석)하고, 실행한다.


### Ammonite

스칼라로 인터프리터를 구현하기 위해서 modernized된 스칼라 인터프리터를 사용할 예정

```scala
import $ivy.`org.scala-lang.modules::scala-parser-combinators:2.4.0`
import scala.util.parsing.combinator._
```