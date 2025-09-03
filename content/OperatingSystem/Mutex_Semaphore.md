
# Mutex (`pthread_mutex_t`) functions

### `pthread_mutex_init()`

`int pthread_mutext_init(pthread_mutext_t *mutex, const pthread_mutexattr_t *attr)`

- `mutex`: 초기화할 mutex 객체 포인터
- `attr`: 속성 (기본값은 `NULL`)
- return value: 성공시 0, 실패 시 에러코드

### `pthread_mutext_destroy()`

`int pthread_mutex_destroy(pthread_mutex_t *mutex)`

- `mutex`: 제거할 mutex 객체 포인터
- 사용 전 unlock된 상태여야 함

### `pthread_mutex_lock()`, `pthread_mutex_unlock()`

`int pthread_mutex_lock(pthread_mutex_t *mutex)`
`int pthread_mutex_unlock(pthread_mutex_t *mutex)`

```c
#include <pthread.h>
#include <stdio.h>

pthread_mutex_t lock;
int shared_counter = 0;

void* increment(void * arg) {
	for(int i=0; i< 100000; i++){
		pthread_mutext_lock(&lock);
		shared_counter++;
		pthread_mutex_unlock(&lock);
	}
	return NULL;
}

int main() {
	pthread_t t1, t2;
	pthread_mutex_init(&lock, NULL);
	
	pthread_create(&t1, NULL, increment, NULL);
	pthread_create(&t1, NULL, increment, NULL);
	
	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Fianl counter: %d\n", shared_counter);
	pthread_mutex_destroy(&lock);

	return 0;
}
```


# Semaphore (`sem_t`) functions

## Named Semaphores
파일 시스템 기반 공유

### `sem_open()`

`sem_t *sem_open(const char *name, int oflag, mode_t mode, unsigned int value)`

- `name`: semaphore name (`/`로 시작해야 함)
- `oflag`: `O_CREAT` | `O_EXCL`
- `mode`: 권한 (ex: `0644`)
- `value`: 초기 세마포어 값

### `sem_close()`

`int sem_close(sem_t *sem)`

- 세마포어 닫기 (연결 해제)

### `sem_unlink()`

`int sem_unlink(const char *name)`

- 이름 삭제


## Unnamed Semaphores
스레드 간 공유

### `sem_init()`

`int sem_init(sem_t *sem int pshared, unsigned int value)`

- `sem`: 세마포어 객체 포인터
- `pshared`: 0이면 같은 프로세스 내 스레드간 공유
- `value`: 초기값

### `sem_destroy`

`int sem_destroy(sem_t *sem)`

- 세마포어 제거


## Common 
공통 함수

### `sem_wait()`

`sem_wait(sem_t *sem)`

- 세마포어 감소 (0이면 대기)

### `sem_post()`

`int sem_post(sem_t *sem)`

- 세마포어 증가 (대기중인 프로세스/스레드 깨우기)


```c
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

// #define SYNC

sem_t sem;
int shared_counter = 0;

void* increase_counter(void* arg){
	for(int i=0; i< 100000; i++){
#ifdef SYNC
		sem_wait(&sem);
#endif
		shared_counter++;
#ifdef SYNC
		sem_post(&sem);
#endif
	}
	return NULL;
}

int main() {

	pthread_t t1,t2;
	sem_init(&sem, 0, 1);

	pthread_create(&t1, NULL, increase_counter, NULL);
	pthread_create(&t2, NULL, increase_counter, NULL);

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Final counter: %d\n", shared_counter);
	sem_destroy(&sem);
	
	return 0;
}
```

