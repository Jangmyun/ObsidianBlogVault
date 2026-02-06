---
title: "\b1_데이터베이스_입문"
description: "DBMS를 통한 간단한 CRUD, SQL 명령어 종류와 데이터 타입\e"
draft: false
tags:
  - DB
---

## 데이터베이스 시작하기

### 데이터베이스 생성하기

```sql
CREATE DATABASE my_shop;
```

데이터베이스는 `CREATE DATABASE` 명령어로 만들 수 있다.
세미콜론 `;`를 하나의 쿼리문으로 인식한다.

### 작업할 데이터베이스 선택하기

```sql
USE my_shop;
```

`USE <데이터베이스이름>` 이후로 실행하는 모든 SQL 명령어는 해당 데이터베이스에 대해 적용된다.

### 테이블 생성

`USE`로 선택한 데이터베이스에 테이블의 구조를 정의하고 생성하는 명령어는 `CREATE TABLE` 이다.

```sql
CREATE TABLE sample (
	product_id INT PRIMARY KEY,
	name VARCHAR(100),
	price INT,
	stock_quantity INT,
	release_date DATE
);
```

`sample` 이라는 이름의 테이블을 생성하는데, `product_id` 열을 PK로 하고 추가적으로 4개의 열로 구성되도록 설정한다.

`INT`, `VARCHAR(100)`, `DATE` 같은 것들은 데이터의 타입을 의미한다.

### 구조 확인

#### 테이블 구조 확인

테이블이 만들어졌는지 확인인하려면 `DESC` 또는 `DESCRIBE`를 사용하면 된다

```sql
DESC sample; -- or DESCRIBE sample;
```

#### DATABASE와 TABLE 목록 확인

```sql
SHOW DATABASES; -- 서버의 모든 데이터베이스 목록
SHOW TABLES;    -- 데이터베이스의 모든 테이블 목록
```

### 삭제

데이터베이스나 테이블을 삭제하려면 `DROP` 을 사용한다.

```sql
DROP TABLE sample; -- sample 테이블 삭제

DROP DATABASE my_shop; -- my_shop 데이터베이스 삭제
```

<br>
---
<br>

## 데이터베이스 CRUD

### 데이터 넣기 (`INSERT`)

```sql
INSERT INTO sample (product_id, name, price, stock_quantity, release_date)
VALUES (1, '프리미엄 청바지', 59900, 100, '2026-02-01');
```

위 SQL문은 `sample` 테이블의 괄호 안 열에 대해 `VALUES` 뒤의 괄호 안 값을 넣어서 새로운 레코드를 생성하라는 의미이다.

### 데이터 읽기 (`SELECT`)

테이블의 데이터를 조회하려면 `SELECT` 를 사용한다.

```sql
SELECT * FROM sample;
```

`*` 는 테이블의 모든 열을 의미한다.

원하는 정보만 보고 싶으면 `SELECT name, price FROM sample;` 처럼 열 이름을 쉼표로 구분하여 지정하면 된다.

### 데이터 수정하기 (`UPDATE`)

```sql
UPDATE sample
SET price = 40000
WHERE product_id = 1;
```

`sample` 테이블에서 `product_id` 가 1인 행의 `price` 를 40000으로 변경한다.

### 데이터 삭제하기 (`DELETE`)

```sql
DELETE sample
WHERE product_id = 1;
```


<br>

---

<br>

## SQL (Structured Query Language)

SQL은 표준이 정해진 RDBMS 표준 언어이다. SQL 표준을 넘어서는 DBMS마다의 고유한 기능이나 추가적인 문법을 **Dialect (방언, 사투리)** 라고 한다.

SQL은 **Declarative Language (선언적 언어)** 이다. DBMS에 어떻게 데이터를 가져올지 지시하는 게 아니라 무엇을 가져와야하는지만 선언적으로 명시한다.

## SQL 명령어의 4가지 종류

### DDL (Data Definition Language, 데이터 정의어)

**DDL**의 목적은 데이터의 **구조**를 정의하고 관리하는 데에 있다.
데이터 자체가 아니라 데이터를 담는 테이블이나 데이터베이스의 설계도를 생성, 수정, 삭제하는 역할을 한다.


#### 주요 명령어

- `CREATE`: 데이터베이스나 테이블 등의 구조를 생성
- `ALTER`: 이미 만들어진 테이블의 구조를 변경
- `DROP`: 데이터베이스나 테이블을 삭제
- `RENAME`: 테이블의 이름 변경 (데이터베이스 이름 변경 방법은 DBMS에 따라 다르다고 한다.)

### DML (Data Manipulation Language, 데이터 조작어)

**DML**의 목적은 테이블 안의 데이터를 조작 (CRUD) 하는 데에 있다.

#### 주요 명령어

DDL로 데이터베이스에서 CRUD 작업을 수행한다.

- `INSERT`: 테이블에 새로운 데이터를 추가 (Create)
- `SELECT`: 테이블에서 데이터를 조회 (Read)
- `UPDATE`: 기존 데이터를 수정 (Update)
- `DELETE`: 기존 데이터를 삭제 (Delete)

### DCL (Data Control Language, 데이터 제어어)

데이터에 대한 접근 권한을 제어하며, 보안과 연관되어 있다.

- `GRANT`: 특정 사용자에게 특정 작업에 대한 권한을 부여
- `REVOKE`: 부여된 권한을 회수


### TCL (Transaction Control Language, 트랜잭션 제어어)

DML에 의해 수행된 데이터 변경 작업들을 하나의 **트랜잭션** 단위로 묶어서 처리할 수 있도록 한다.
일련의 작업들은 모두 성공하거나, 하나라도 실패하면 트랜잭션으로 묶인 모든 변경사항들이 취소되어야 한다.

- `COMMIT`: 트랜잭션의 모든 작업을 최종적으로 데이터베이스에 확정하여 저장
- `ROLLBACK`: 트랜잭션의 작업을 모두 취소하고 이전 상태로 변경


<br>

---

<br>

## 데이터 타입



<br>

---

<br>

## 제약조건