 # CPU Scheduling

## Basic Concepts

### Motivation
멀티프로그래밍, 멀티태스킹 상황에서 **CPU utilization**을 극대화

![[Screenshot 2025-04-29 at 13.50.36.png]]

## CPU-I/O Burst Cycle

프로세스 실행은 CPU실행과 I/O 대기의 사이클

> 처음과 마지막 burst는 CPU burst이다.

![[Screenshot 2025-04-29 at 13.58.35.png]]
### 프로세스 타입
- I/O-bound process
	- CPU bursts가 짧게 많이
- CPU-bound process
	- CPU bursts가 길게 조금

![[Screenshot 2025-04-29 at 13.57.19.png]]

## CPU Sheduler

### CPU scheduler (= short term scheduler)
Ready queue로부터 실행할 프로세스를 선택하여 CPU에 할당

### Ready queue의 구현

FIFO, **Priority queue**, tree, unordered linked list

각 프로세스는 PCB로 표현


## Preemptive Scheduling 선점형 스케줄링

프로세스가 실행중인동안 스케줄링 발생 가능
(강제로 프로세스의 CPU 사용을 중단시키고 다른 프로세스에 CPU 할당)

ex) 인터럽트나 더 높은 우선순위의 프로세스

## 스케줄링의 발생시점

1. 프로세스가 running 상태에서 waiting 상태로 전환될 때
2. 프로세스가 running 상태에서 ready 상태로 전환될 때
3. 프로세스가 waiting 상태에서 ready 상태로 전환될 때
4. 프로세스가 종료될 때

![[Screenshot 2025-04-29 at 14.09.41.png]]

1번과 4번은 필수
2번과 3번은 스케줄링 방식에 따라 선택적이다.

non-preemptive의 경우 2번 3번 경우에 스케줄링이 발생하지 않고 프로세스가 스스로 CPU를 반납할 때까지 기다린다.

## Preemptive Scheduling

### Non-preemptive scheduling
위 스케줄링 케이스 1,4번에서만 스케줄링 발생
실행중인 프로세스는 interrupted 되지 않는다.

### Preemptive scheduling
1,2,3,4번 케이스에서 모두 스케줄링 발생
프로세스 실행중에 스케줄링이 발생할 수 있음
하드웨어 지원과 shared data handling 필요

**Preemptive scheduling**은 프로세스간 데이터를 공유할 때 **race condition**을 야기할 수 있다.

## Preemption of OS Kernel

### Preemptive kernel
커널이 시스템 콜 중 preemption 허용

-> real-time (반응성이 중요한 프로그램) support할 때 좋음

근데 대부분의 OS에서 시스템은 non-preemptive임

## Dispatcher

### Dispatcher
short-term 스케줄러에 의해 선택된 프로세스에세 CPU 제어권을 넘겨주는 모듈

- Switching context
- Switching to user mode
- Jumping to proper location in user program


### Dispatch latency
프로세스 중단부터 다른 프로세스 시작까지의 시간

![[Screenshot 2025-04-29 at 14.44.02.png]]


## Scheduling Criteria

- CPU utilization: CPU를 최대한 바쁘게
- Throughput: 시간 단위 당 완료된 프로세스의 수
- Turnaroundtime: 프로세스 제출부터 완료시점까지의 시간
- Waiting time: Ready Q에서 대기한 시간의 함
- Response time: 요청 제출 시점부터 첫 번째 응답이 나올 때까지의 시간

---
# Scheduling Algorithms

## First-come, first-served (FCFS) scheduling

> CPU에 먼저 요청한 놈이 먼저 served

Non-preemptive scheduling
가장 단순한 스케줄링 방법

근데 비효율을 곁들인

![[Screenshot 2025-04-30 at 11.38.40.png]]

## Shortest-Job-First (SJF) scheduling

> Burst time이 가장 짧은 프로세스를 선택

SJF는 waiting time의 관점에서 최적이다.

문제는 다음 CPU burst의 길이를 알기 어렵다는 것
-> 그동안 쌓인 burst time 기록을 기반으로 비슷하게 구현할 수 있음

![[Screenshot 2025-04-30 at 11.41.27.png]]

### Exponential averaging

![[Screenshot 2025-04-30 at 11.57.28.png]]

- `t_n`: n번째 CPU burst의 실제 길이
- `τ_n`: n번째 CPU burst의 예측값
- `α`: 0과 1사이의 값
	- `α = 0`: n번째 CPU burst의 실제 길이를 무시
	- `α = 1`: n번째의 예측값만으로 n+1을 예측
	- 보통 `α = 0.5` 사용

![[Screenshot 2025-04-30 at 12.01.23.png]]

### Preemptive version of SJF scheduling

![[Pasted image 20250430120335.png]]

## Priority Scheduling

> Priority가 가장 높은 프로세스에 CPU 할당

- priority가 같은 프로세스들 끼리의 priority scheduling은 FCFS와 같다

![[Screenshot 2025-04-30 at 12.13.16.png]]

### Priority can be assigned **internally** and **externally**

#### Internally
determined by measurable quantity or qualities

커널이 봤을 때 CPU burst가 짧게 자주 쓰이는 I/O-bound 프로세스 (real time이 중요한 프로세스) 를 위주로 선택

ex) time limit, memory requirement, # of open files, ratio of I/O burst and CPU burst, ...
#### Externally
importance, political factors


> Priority scheduling은 preemptive, non-preemptive 둘 다 가능하다

### Major problems

#### Indefinite blocking (starvation)
priority가 낮은 프로세스는 CPU 자원을 할당받지 못하는 문제

**aging**을 통해 오랫동안 waiting 상태인 프로세스의 priority를 점점 증가시킨다.

## Round-Robin (RR) Scheduling

> FCFS랑 비슷한데, 이제 preemptive 인..

- time-sharing system을 위함
- CPU time을 **time quantum (time slice)**로 나눔
- Ready queue를 **circular queue**로 취급
- CPU scheduler는 1 ready queue를 돌면서 time quantum만큼의 시간을 부여

![[Screenshot 2025-04-30 at 12.50.09.png]]

RR 스케줄링의 성능은 time quantum size에 의존적
- time quantum이 매우 짧음 = processor sharing
- time quantum이 매우 김 = FCFS

Turnaround time도 time quantum size에 의존적
- avg turnaround time은 time quantum size에 정비례하거나 반비례하지 않음 (time quantum 사이즈 조정이 turnaroun time을 좋게 하거나 나쁘게 하지 않는다)
- 대부분의 프로세스가 cpu burst를 한 time quantum 내에 완료하면 turnaround time 향상

### A rule of thumb
80%의 CPU burst가 time quantum보다 짧아야 한다.

![[Screenshot 2025-04-29 at 13.57.19.png]]


## Multilevel Queue Scheduling

프로세스를 그룹으로 분류하고 서로 다른 스케줄링 전략을 사용

ready queue를 여러개의 queue로 분할

![[Screenshot 2025-04-30 at 17.52.14.png]]

각 queue는 자기들만의 스케줄링 알고리즘이 존재한다.

### Scheduling among queues

#### Fixed-priority preemptive scheduling
낮은 우선순위 큐의 프로세스는 높은 우선순위 큐가 비어있을 때만 실행가능

후보들 중 우선순위가 높은 프로세스를 선택
#### Time-slicing among queues
각 queue에 CPU time의 일정비율을 할당

ex)<br>foreground queue(interactive processes): 80%<br>background queue(batch processes): 20%

`Assignment of a queue to a process is permanent`
한번 어떤 queue에 들어가면 다른 queue로 이동할 수 없다



## Multilevel Feedback-Queue Scheduling

multilevel queue scheduling과 비슷한데, 이제 프로세스가 queue간에 이동가능한..

### Idea: **CPU burst 특성에 따라 프로세스를 분리**

**CPU time을 너무 많이 사용하는 프로세스**를 더 낮은 우선순위의 큐로 이동
**I/O-bound (interactive) 프로세스**는 더 높은 우선순위의 큐로 이동

![[Screenshot 2025-04-30 at 18.55.14.png]]

### Parameters to define a multilevel feedback-queue scheduler

- `#` of queue
- Scheduling algorithm for each queue
- Method to determine when to upgrade a process to higher priority queue
- Method to determine when to demote a process to lower priority queue
- Method to determine which queue a process will enter when it needs service


---
# Multiple -processor scheduling

## Multiple-Processor Scheduling

### Multiple-processor system

load balancing 가능
스케줄링이 복잡해진다 (하던 프로세스가 하던일 계속하는 게 좋다 (캐싱이슈))

해당 책에서는 **Symmetric Multiprocessing** 시스템이라고 가정

### Two possible strategies

1. 모든 스레드가 하나의 common ready에 있을 수 있음
2. 각 프로세서별로 자체적인 개인 스레드 큐를 가질 수 있음

![[Pasted image 20250430192929.png]]

## Processor Affinity 프로세서 친화성

하나의 프로세서에서 다른 프로세서로 프로세스를 이동시키는 데에는 오버헤드가 있음.
`migration overhead`
캐시 내용이 쓸모없어지고 다시 채워야함

### Processor Affinity

migration 오버헤드를 피하기 위해 프로세스를 동일한 프로세서에서 계속 실행하도록 한다

#### Soft affinity
OS가 동일한 프로세서에서 프로세스를 실행하려고 하는데, 마이그레이션은 가능함

#### Hard affinity
프로세스의 마이그레이션을 막을 수 있음

### NUMA (Non-Uniform Memory Access)
에서는 affinity가 특히 중요하다
프로세서마다 로컬 메모리가 있고 서로 메모리 접근할 때 느릴 수 있기 때문

## Load balancing

> 모든 프로세서에 workload를 이븐하게 분배

#### Push migration
주기적으로 각 프로세서의 load 확인
언밸런스하면 프로세스를 덜 바쁜 프로세서로 이동 (일을 떠맡김)
#### Pull migration
유휴 프로세서가 대기중인 작업을 가져옴

`위 두 migration 방법은 병렬로 구현가능`

`로드 밸런싱과 프로세서 affinity는 서로의 장점을 상쇄할 수도 있음`

## Multi-core Processor

### Scheduling issues on multi-core processor

#### Memory stall
메모리 접근 시 데이터가 사용 가능해질 때까지 상당한 시간이 소요
ex) 캐시에 없는 데이터에 접근할 때

멀티스레드 프로세서 코어로 **memory stall** 해결가능

![[Screenshot 2025-04-30 at 20.52.07.png]]

---

# Thread scheduling

## Thread scheduling

### Threads

- User thread: 스레드 라이브러리가 제공
	- **LWP**에 의해 간접적으로 스케줄링
- Kernel thread: OS 커널이 제공 (**실제 스케줄링 단위**)

운영체제는 사실 프로세스가 아니라 커널 스레드를 스케줄링하는 거임

## Contention Scope 경쟁범위

### Process-contention scope (PCS)

- 사용자 스레드 간 LWP competetion
	- many-to-one 또는 many-to-many
		- 스레드 라이브러리가 어떤 사용자 스레드에 LWP 할당할지 결정
- Priority based

### System-contention scope (SCS)

- 커널 스레드 간 CPU competition

![[Screenshot 2025-04-30 at 21.14.54.png]]

## Pthread Scheduling

pthread 만들 때 `PCS`와 `SCS`를 지정할 수 있다

- PCS: `PTHREAD_SCOPE_PROCESS`
- SCS: `PTHREAD_SCOPE_SYSTEM`

### functions

`pthread_attr_setscope(pthread_attr_t *attr, int scope)`
`pthread_attr_getscope(pthread_attr_t *attr, int *scope)`

#### 예제
```c
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>

void* runner(void* arg){
	printf("thread runner\n");
	return NULL;
}

int main() {

	pthread_t tid = 0;
	pthread_attr_t attr;
	int scope = 0;

	pthread_attr_init(&attr);

	pthread_attr_getscope(&attr, &scope);
	printf("pthread attr scope: %d\n", scope);
	
	if(scope == PTHREAD_SCOPE_PROCESS){
		printf("PTHREAD_SCOPE_PROCESS\n");
	}else if(scope == PTHREAD_SCOPE_SYSTEM) {
		printf("PTHREAD_SCOPE_SYSTEM\n");
	}

	pthread_create(&tid, &attr, runner, NULL);

	pthread_join(tid, NULL);

	return 0;
}
```


## Real-time CPU Scheduling

### Real-time Operating Systems (RTOS)
- real-time 시스템을 지원하기 위해 설계된

#### Soft real-time systems
- critical real-time 프로세스가 언제 스케줄링 될지에 대한 보장 없음
- noncritical 프로세스보다 먼저 처리될 것이라는 보장은 됨

#### Hard real-time systems
task가 deadline안에 무조건 처리돼야 함
deadline 못지키면 처리 안된 것. (시스템 오작동 가능성 있)

> 대부분의 real-time 시스템은 **event-driven 시스템**이다.

### Event latency
이벤트 발생 시점부터 처리 시점까지 경과한 시간
![[Screenshot 2025-05-05 at 14.28.16.png]]

이벤트 레이턴시는 짧을수록 좋다

### Interrupt Latency
CPU에 인터럽트가 도착한 시점부터 해당 인터럽트 서비스 루틴이 시작하기까지 걸리는 시간
![[Screenshot 2025-05-05 at 14.30.22.png]]

### Dispatch Latency
스케줄링 디스패처가 프로세스를 중단하고 다른 프로세스를 실행하는 데 걸리는 시간

> **preemptive 커널**은 dispatch latency를 낮게 유지하는 가장 효율적인 테크닉

![[Screenshot 2025-05-05 at 14.32.27.png]]

#### Conflict phase 충돌 단계
1. Preemption of any process running in the kernel (커널에서 실행중인 모든 프로세스의 선점)
	1. 높은 우선순위의 실시간 프로세스가 준비 상태가 되었을 때, 만약 현재 커널 모드에서 실행 중인 낮은 우선순위의 프로세스가 있다면, 이 프로세스의 실행을 즉시 중단시키는 과정입니다. 선점형 커널에서는 시스템 호출과 같은 커널 코드 실행 중에도 더 높은 우선순위의 프로세스가 도착하면 선점이 발생할 수 있습니다
2. Release of resources occupied by low-priority processes needed by a high-priority process (높은 우선순위 프로세스가 필요로 하는 자원을 낮은 우선순위 프로세스가 점유하고 있는 경우, 해당 자원을 해제하는 과정)
	1. 높은 우선순위의 프로세스가 실행되기 위해 특정 자원 (예: 뮤텍스, 세마포어, 공유 메모리)을 필요로 하지만, 현재 낮은 우선순위의 프로세스가 이 자원을 점유하고 있는 경우, 낮은 우선순위 프로세스가 자원을 반납할 때까지 높은 우선순위 프로세스는 대기해야 합니다. 자원 경합이 발생하면 디스패치 지연 시간이 늘어날 수 있습니다. 특히 우선순위 역전 (priority inversion)과 같은 문제가 발생하면 예측 불가능한 지연이 발생할 수 있습니다

## Priority-based Scheduling

`RTOS`에서 가장 중요한 특징은 real-time 프로세스에 즉시 응답하는 것이다.
따라서 스케줄러는 **priority-based preemptive** 알고리즘을 지원해야 함

**priority-based preemptive** 스케줄러는 soft real-time 기능만 보장한다.
#### Hard real-time system
**Hard real-time system**은 real-time task가 마감시간 requirements에 따라 처리될 것이라는 것을 추가적으로 보장해야 한다.



















#### 예제

```c
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>

#define NUM_THREADS 3

void* runner(void* arg){
	printf("thread\n");
	return NULL;
}

int main() {
	int i=0, policy =0;
	pthread_t tid[NUM_THREADS]= {0};
	pthread_attr_t attr;

	pthread_attr_init(&attr);

	if(pthread_attr_getschedpolicy(&attr, &policy) != 0){
		fprintf(stderr, "Unable to get policy\n");
	} else {
		if(policy == SCHED_OTHER){
			printf("SCHED OTHER\n");
		}else if(policy == SCHED_RR){
			printf("SCHED_RR\n");
		}else if(policy == SCHED_FIFO){
			printf("SCHED_FIFO\n");
		}
	}

	if(pthread_attr_setschedpolicy(&attr, SCHED_FIFO)!=0){
		fprintf(stderr, "Unable to set policy\n");
	}

	for(i=0; i<NUM_THREADS; i++){
		pthread_create(&tid[i], &attr, runner, NULL);
	}

	for(i=0; i<NUM_THREADS; i++){
		pthread_join(tid[i], NULL);
	}

	return 0;
}
```






