# exec 계열

`execlp()`

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork 실패");
        return 1;
    }

    if (pid == 0) {
        // 자식 프로세스
        execlp("ls", "ls", "-l", NULL);
        perror("execlp 실패"); // execlp가 실패하면 이 줄이 실행됨
    } else {
        // 부모 프로세스
        wait(NULL);
        printf("자식 프로세스 종료됨\n");
    }

    return 0;
}
```

`execvp()`
```c
char *args[] = {"ls", "-a", NULL};
        execvp("ls", args);
        perror("execvp 실패");
```

# Producer-Consumer circular queue
```c
typedef struct{

}item;

item buffer[BUFFER_SIZE];
int in =0;
int out = 0;

// empty/full condition
in == out; // empty
(in + 1)%BUFFER_SIZE == out; // full

// insert
buffer[in] = newItem;
in = (in + 1)%BUFFER_SIZE;

// extract
item = buffer[out];
out = (out + 1)%BUFFER_SIZE;
```

# Producer-Consumer Bounded Buffer
```c

// producer

item nextProduced;

while(1){
	// produce an item in nextProduced
	while((in+1)%BUFFER_SIZE == out); // waiting

	buffer[in] = nextProduced;
	in = (in+1)%BUFFER_SIZE;
}


// consumer

item nextConsumed;

while(1){

	while(in==out); // waiting
	nextConsumed = buffer[out];
	out = (out+1)%BUFFER_SIZE;
}
```

spin lock을 사용하기 때문에 CPU를 소모


# System-v shared memory
```c
#
```
