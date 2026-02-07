---
title: Unity - Time.deltaTime
description: Time.deltaTime 이란
draft: false
tags:
  - Unity
---

컴퓨터마다 사양이 다르기 때문에 게임의 FPS가 달라지고, 매 프레임마다 실행되는 `Update` 함수가 실행되는 횟수도 달라진다.

`Update` 함수에서 플레이어의 `transform.position`을 변경하는 작업을 수행하게 되면, 컴퓨터마다 FPS가 다르기 때문에 플레이어가 움직이는 속도도 달라질 것이다.

## `Time.deltaTime`

`Time.deltaTime`은 각 프레임을 렌더링하는데 걸리는 시간이다.

예를들어 FPS가 100이면 초당 100번 프레임이 바뀌는 것이고, 시간은 1/100으로 `deltaTime`은 0.01이 되겠다.


`Time.deltaTime`은 FPS에 관계없이 캐릭터의 이동 속도를 일정하게 만드는 데 사용할 수 있다.

```cs
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float _speed = 10.0f;
    void Start()
    {

    }

    void Update()
    {

        if (Input.GetKey(KeyCode.W)) transform.position += new Vector3(0f, 0f, 1.0f) * Time.deltaTime * _speed;
        if (Input.GetKey(KeyCode.S)) transform.position += new Vector3(0f, 0f, -1.0f) * Time.deltaTime * _speed;
        if (Input.GetKey(KeyCode.A)) transform.position += new Vector3(-1.0f, 0f, 0f) * Time.deltaTime * _speed;
        if (Input.GetKey(KeyCode.D)) transform.position += new Vector3(1.0f, 0f, 0f) * Time.deltaTime * _speed;
    }
}
```

WASD 키를 사용해 캐릭터를 상하좌우로 이동하는 로직이다. 



A 컴퓨터는 100 FPS, B 컴퓨터는 10 FPS 라고 가정하고, `Update` 함수에서 캐릭터의 position을 `1.0f` 이동하려고 한다.

1초동안 컴퓨터 A와 B의 이동 거리를 비교해보자.

- 컴퓨터 A: `1.0f * 100번 실행` = 100m 이동
- 컴퓨터 B: `1.0ㄹ * 10번 실행` = 10m 이동

컴퓨터가 좋을수록 이동속도가 빠른 말도 안되는 문제가 발생한다.

여기에 `Time.deltaTime` 을 곱해보자.

- 컴퓨터 A: `(1.0f * 0.01초) * 100번 실행` = 1m 이동
- 컴퓨터 B: `(1.0f * 0.1초) * 10번 실행` = 1m 이동

놀랍게도, FPS가 달라도 1초동안 같은 거리를 이동한다.


### 핵심

`Time.deltaTime`은 프레임을 렌더링하는 데 걸린 시간이라고 했다.

- FPS 100이면 `deltaTime`은 0.01이다. 둘이 곱하면 1이다.
- FPS 10이면 `deltaTime`은 0.1이다. 마찬가지로 곱하면 1이다.

즉 **`deltaTime` 은 프레임당 움직임을 시간당 (초당) 움직임으로 바꿔주는 도구** 라고도 말할 수 있겠다.