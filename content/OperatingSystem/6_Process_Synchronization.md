1. Background
2. The critical-section problem
3. H/W Support for Synchronization
4. Mutex and Semaphore
5. Monitors
6. Liveness

### Background

Process Communication 방법
- Message passing
- **Shared memory** (confliction  발생 가능)

Producer-consumer problem
![[Screenshot 2025-05-29 at 02.25.30.png]]

## Concurrent Access of Shared Data
공유 데이터에 동시에 접근했을 때 문제

```c
// 생산자 (Producer)
while(true){
    while(counter == BUFFER_SIZE); // 버퍼가 가득 차면 대기 (공간이 생길 때까지)
    buffer[in] = nextProduced;    // 생산된 아이템을 버퍼에 넣기
    in = (in + 1) % BUFFER_SIZE;  // 'in' 포인터 업데이트
    counter++;                     // 카운터 증가
}

// 소비자 (Consumer)
while(true){
    while(counter == 0);          // 버퍼가 비어 있으면 대기 (아이템이 생길 때까지)
    nextConsumed = buffer[out];   // 버퍼에서 아이템 가져오기
    out = (out + 1) % BUFFER_SIZE; // 'out' 포인터 업데이트
    counter--;                     // 카운터 감소
}
```

`counter`의 증가/감소 연산할 때, 기계어 수준에서 레지스터로 `counter`값을 fetch하고 그 값에 증가/감소 연산을 한 이후 다시 메모리의 `counter`변수에 writing한다.

modification(수정) 작업동안 스케줄러에 의한 context switching이 발생할 수 있다.
이때 **Race Condition**이 발생할  수 있다. (데이터 불일치)

해결을 위해서는 **Synchronization**을 보장 해야한다.

### Race condition
여러 프로세스가 동시에 동일한 데이터에 접근하여 조작하는 상황

Execution의 결과가 공유 데이터에 접근하는 순서에 따라 달라지는 상황

### Synchronization
공유 자원에 접근할 때 실행순서를 제어하여 **race condition**이 발생하지 않도록 함
-> 한번에 하나의 프로세스만 공유 데이터에 접근할 수 있도록 보장


## The Critical-Section Problem

### Critical-Section Problem
프로세스가 cooperate 할 수 있는 프로토콜을 설계

n개의 프로세스가 시스템에서 동시에 실행되고 있을 때
각 프로세스는 다음과 같이 구성된다.

#### Critical-Section
공유 리소스에 접근하거나 변경할 수 있는 코드 세그먼트
**race condition**을 피하려면 **critical section**에는 오직 하나의 프로세스만 진입하도록 보장
#### Remainder section
공유자원을 변경하지 않는 코드 세그먼트

#### Entry section
critical section에 진입 허가를 요청하는 코드 섹션

#### Exit section
critical section을 떠났음을 알리는 코드 섹션

![[Pasted image 20250603232829.png]]

### Requirements of Critical-Section Problem

#### Mutual exclusion
한 프로세스가 크리티컬 섹션에서 실행중이라면 다른 프로세스는 크리티컬 섹션에서 실행될 수 없다. (대기해야 함)

#### Progress
critical section이 비어있으면 무한정 대기 없이 waiting중인 프로세스들 중 하나가 진입해야한다

Critical section에서 실행중인 프로세스가 없을 때, Remainder section에서 실행중이지 않은 프로세스들만이 다음 Critical section에 진입할 프로세스 결정에 참여할 수 있다.

#### Bounded waiting
**starvation**방지를 위해
한 프로세스가 critical section 진입 요청을 한 후부터 그 요청이 허가될 때까지 다른 프로세스들이 자신의 critical section에 진입하는 횟수에 제한이 존재해야한다.

### Kernel is an example of critical section problem

커널은 프로세스와 스레드가 공유하는 핵심 데이터 구조와 리소스를 관리

#### Non-preemptive 
프로세스가 커널모드에서 실행중일 경우 context switching 이 발생할 수 없다.

race condition으로부터 자유롭다.

#### Preemptive kernel
critical section 문제를 해결한 preemptive kernel은

real-time programming에 더 적합 (응답성이 좋다.)

## Peterson's Solution
critical section problem을 해결하기 위한 S/W적 솔루션
`load/store` 명령어 때문에 일부 아키텍쳐에서 정상 작동 보장x

- `P_0`과 `P_1` 프로세스
- `int turn`: 어떤 프로세스가 critical section에서 실행되도록 허용 됐는지 (initial=0)
- `boolean flag[2]`: `flag[i]`가 true면 `P_i`는 critical section에 들어갈 준비됨

### Erroneous Algorithm 1

#### P_i
```c
do {
	while (turn != i); // 자신 차례가 될 때까지 대기
	// critical section
	turn = j; // 상대방 턴으로 넘기기
	// remainder section
} while (1);
```

#### P_0
```c
do {
    while (turn != 0); // turn이 0이 될 때까지 대기
    //critical section
    turn = 1;          // P1에게 차례 넘기기
    //remainder section
} while (1);
```

#### P_1
```c
do {
    while (turn != 1); // turn이 1이 될 때까지 대기
    //critical section
    turn = 0;          // P0에게 차례 넘기기
    //remainder section
} while (1);
```

위 패턴은 **mutual exclusion**은 보장되지만 **progress**는 보장되지 않음

#### 시나리오
1. turn = 0`으로 시작
2. P0 실행되어 critical section에서 작업 완료 후 `turn = 1`
3. `turn == 1`이지만 P1이 critical section에 진입할 의사가 없음
4. P0가 remainder section을 마치고 다시 critical section에 들어가고자 하지만 P1이 `turn = 0`을 실행할 때까지 대기해야함.


### Erroneous Algorithm 2
#### P0
```c
do {
    flag[0] = true;     // P0이 진입 의사 알림
    while(flag[1]);     // P1이 진입 의사가 있는지 확인
    //critical section
    flag[0] = false;
    //remainder section
} while (1);
```

#### P1
```c
do {
    flag[1] = true;     // P1이 진입 의사 알림
    while(flag[0]);     // P0이 진입 의사가 있는지 확인
    //critical section
    flag[1] = false;
    //remainder section
} while (1);
```

위 패턴은 **mutual exclusion**은 보장되지만 **progress**는 보장되지 않음

#### 시나리오
1. P0와 P1이 거의 동시에 실행되어 `flag[0]`과 `flag[1]`이 모두 `true` 
2. P0와 P1 모두 `while(flag[j])`에서 무한 대기 상태에 빠짐

### Peterson's Solution

*Peterson's solution*은 세 개의 conditions를 모두 보장한다.
#### P0
```c
do {
    flag[0] = true;             
    turn = 1;                   
    while (flag[1] && turn == 1);
    // critical section            
    flag[0] = false;            
    // remainder section           
} while (1);
```

#### P1
```c
do {
    flag[1] = true;             
    turn = 0;                   
    while (flag[0] && turn == 0);
    // critical section            
    flag[1] = false;            
    // remainder section           
} while (1);
```

#### Mutual Exclusion 증명

P0과 P1이 동시에 critical section에 진입했다는 것은
- P0이 `while(flag[1] && turn == 1)`를 통과함
- P1이 `while(flag[0] && turn == 0)`를 통과함
을 의미함

`flag[0] = flat[1] = true`s
`turn`변수는 0이면서 동시에 1일 수 없다.


#### Progress, Bounded Waiting 증명

- `Pi`의 blocking 조건: `while(flag[j]==true && turn ==j);`
	- `Pj`가 critical section에 진입할 의사가 있고, `Pj`에게 차례가 넘어갔을 때만 대기
- **Case 1**: `Pj`가 `flag[j] == false`일 때 (critical section 진입할 의사가 없는 경우)
	- `Pi`의 while 조건이 `false`가 되어 바로 critical section 진입
- **Case 2**: `Pj`가 `flag[j] == true`일 때 (critical section에 진입하고자 할 경우)
	- `flag[i] = flag[j] = true`이고 `turn`은 `Pi`와 `Pj`중 마지막으로 썼는지에 따라 결정
		- `turn == i`면 `Pj`는 대기, `Pi`는 critical section 진입
		- `turn == j`면 `Pj`가 critical section 진입

`Pj`가 critical section에서 작업을 마치고 `flag[j] = false`를 실행하면 그 순간 `Pi`의 while문이 `false`가 되어 critical section에 진입가능함.

어떤 경우든 `Pi`나 `Pj`중 하나는 while문을 통과하여 critical section에 진입 (**Progress**)

최대 한 번만 기다리면 critical section에 진입가능함 (**Bounded waiting**)

### Peterson's Solution의 문제

현대 컴퓨터 아키텍처에서는 동작을 보장하지 않는다.

- 시스템 퍼포먼스 향상을 위해 프로세서 또는 컴파일러는 읽기/쓰기 연산을 **reorder**할 수 있다.
- 공유 데이터를 사용하는 멀티스레드 앱의 경우 명령어 재배열로 인해 예상치 못한 결과가 나올 수 있다.


## H/W Support for Synchronization

### Memory Model
Memory model: how a computer architecture determines what memory guarantees it will provide to an application program.

컴퓨터 아키텍처가 프로그램에 어떤 메모리 보장을 제공할 것인지 결정하는 방법

#### Strongly ordered
한 프로세서에서 발생한 메모리 수정이 다른 모든 프로세서에서 즉시 **visible**

#### Weakly ordered
메모리 수정이 다른 프로세서에게 즉시 visible하지 않을 수 있다.

### Memory Barriers (Memory fences)

메모리의 모든 변경 사항이  다른 프로세서로 propageted 되도록 강제할 수 있는 instruction

### Hardware Instructions
Critical Section problem은 **lock**을 통해 방지
```c
do {
    acquire lock; // lock 획득  
	    // critical section;   
    release lock; // lock 해제
	    // remainder section;  
} while(TRUE);
```

### Mutual Exclusion by Lock Variable
공유 변수 `lock` 을 통해 **mutual exclusion**을 보장하기

- `Boolean lock = 0`
- `lock`이 `false`면 어떤 프로세스든 critical section에 진입 가능
- 프로세스가 critical section에 진입할 때 `lock`을 `true`로

#### P0, P1
```c
do {
    while(lock);      
    lock = true;      
	    // critical section
    lock = false;     
	    // remainder section
} while(TRUE);
```

checking과 locking이 **원자성(atomicity)** 을 보장하지 않으면 mutual exclusion을 보장할 수 없다.

### Interrupt Disable
single processor 시스템에서는 **disabling interrupt**로 critical section problem을 해결 = **Non-preemptive kernel**

#### problems
- 멀티 프로세서 환경에서 비효율
- 일부 시스템에서는 클럭이 인터럽트에 의해 업데이트된다.

### Hardware Instructions

하드웨어에서 **atomic instruction**을 제공한다면 locking을 구현하기 쉬움

`boolean lock = false;`
#### TestAndSet
```c
boolean TestAndSet(boolean *target) {
	boolean rv = *target;
	*target = true;
	return rv;
}
```

```c
do {
	while(TestAndSet(&lock));
	// critical
	lock = false;
	// remainder
} while (1);
```
#### Swap
```c
void Swap(boolean *a, boolean *b){
	boolean temp = *a;
	*a = *b;
	*b = temp;
}
```

```c
do {
	key = true; // local var
	while(key == true)
		Swap(&lock, &key);
	// critical
	lock = false;
	// remainder
} while (1);
```
#### CompareAndSwap
```c
int CompareAndSwap(int *value, int expected, int new_value){
	int temp = *value;
	if(*value == expected)
		*value = new_value;
	return temp;
}
```

```c
while(true) {
	while(CompareAndSwap(&lock, 0, 1) != 0);
	// critical
	lock = 0;
	// remainder
}
```

### Bounded Waiting Mutual Exclusion

N 개의 프로세스를 위한 Bounded waiting
![[Screenshot 2025-06-10 at 22.22.12.png]]
P0, P1, P3, P5는 critical section에 진입하기를 원하는 상황에서 Bounded waiting을 보장

`boolean lock;`
`boolean waiting[n]`

```c
while(TRUE){
	waiting[i] = TRUE;
	key = TRUE; // local var
	while(waiting[i] && key)
		key = TestAndSet(&lock);
	waiting[i] = FALSE;

	// critical

	j = (i+1) % n;
	while(j!=i && !waiting[j])
		j = (j+1) % n;

	if(j==i)
		lock = FALSE;
	else
		waiting[j] = FALSE;
	
	// remainder
}
```

```c
while(true) {
    // 1. 진입 구역 (Entry Section)
    waiting[i] = true; // Pi가 임계 구역 진입을 원한다고 표시
    int key = 1;       // 지역 변수 'key'를 1로 초기화 (CAS 시도 신호)

    // waiting[i]가 true이고 key가 1인 동안 반복 (바쁜 대기)
    // CAS가 lock을 0에서 1로 성공적으로 변경하고 0을 반환하면 루프 탈출
    while (waiting[i] && key) {
        key = compare_and_swap(&lock, 0, 1);
    }
    waiting[i] = false; // 임계 구역 진입이 허가되었으므로 대기 상태 아님을 표시

    /* critical section */ // 2. 임계 구역 (Critical Section)
    // 공유 데이터 접근 및 수정

    // 3. 퇴출 구역 (Exit Section)
    j = (i + 1) % n; // 다음 차례 프로세스를 i+1부터 순환적으로 탐색 시작

    // j가 다시 i가 되거나, waiting[j]가 true인 프로세스를 찾을 때까지 순환 탐색
    while ((j != i) && !waiting[j]) {
        j = (j + 1) % n;
    }

    if (j == i) {      // (a) 모든 프로세스를 순회했지만, 대기 중인 다른 프로세스가 없는 경우
        lock = 0;      // 락을 해제하여 임계 구역을 자유롭게 만듦
    } else {           // (b) 대기 중인 다음 프로세스 Pj를 찾은 경우
        waiting[j] = false; // Pj에게 임계 구역에 진입해도 좋다는 "허가"를 줌
                            // Pj는 자신의 while(waiting[j] && key) 루프를 통과할 수 있게 됨
    }

    /* remainder section */ // 4. 나머지 구역 (Remainder Section)
    // 임계 구역과 관련 없는 작업
}
```

![[Screenshot 2025-06-10 at 22.34.44.png]]

### Atomic Variables
int나 bool같은 기본 데이터 타입에 **atomic operation**을 제공

mutual exclusion 보장을 위해 사용가능

**Compare And Swap**(CAS) 같은 atomic instruction으로 구현됨


