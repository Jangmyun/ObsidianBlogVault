---
title: 2. 데이터베이스 입문 - DDL
description: 테이블 생성
draft: true
tags:
  - DB
---

## DDL

### 테이블 생성

```sql
CREATE TABLE customers (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
	address VARCHAR(255) NOT NULL,
	join_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

- `AUTO_INCREMENT`: 테이블에 새 레코드가 INSERT 될 때마다 자동으로 순차적으로 숫자를 생성해주는 기능
- `DEFAULT CURRENT_TIMESTAMP`: 값을 따로 넣지 않으면 기본값으로 현재 시각이 기록되도록 한다.

### 날짜와 기본값 설정 옵션

```sql
CREATE TABLE date_time (
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

- `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
	- 새로운 레코드가 추가될 때는 현재 시각, 같은 레코드의 값이 변경될 때 (`UPDATE`) 갱신


### 외래 키 제약 조건 

외래 키는 참조 무결성 특징을 갖는다
- **데이터 일관성**: 부모 테이블에 없는 값은 자식 테이블에 입력할 수 없다.
- **중복 허용**: 외래 키는 중복을 허용한다.

```sql
CONSTRAINT [제약조건_이름]
FOREIGN KEY ([자식_테이블의_컬럼명])
REFERENCES [부모_테이블명]([부모_테이블의_컬럼])
[ON DELETE 옵션] [ON UPDATE 옵션]
```


```sql
CREATE TABLE products (
	product_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	price INT NOT NULL,
	stock_quantity INT NOT NULL DEFAULT 0
);
```


```sql
CREATE TABLE orders (
	order_id INT AUTO_INCREMENT PRIMARY KEY,
	customer_id INT NOT NULL,
	product_id INT NOT NULL,
	quantity INT NOT NULL,
	order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	status VARCHAR(20) NOT NULL DEFAULT '주문접수',
	
	CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id)
		REFERENCES customers(customer_id),
	
	CONSTRAINT fk_orders_products FOREIGN KEY (product_id)
		REFERENCES products(product_id)
);
```

- orders 테이블에서 `customer_id`, `product_id` 은 외래 키 연결을 위한 컬럼이다.
