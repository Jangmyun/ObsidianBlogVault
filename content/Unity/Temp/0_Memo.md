---
title: Example Title
description: Example Description
draft: true
tags:
  - Unity
---
 
배운 내용 - 

Unity 공부 내용

[SerializedField]

private int speed _speed;

다음처럼 private 변수위에 SerializedField 붙이면 유니티 툴에서 수정가능하게 변경됨

transform.TransformDirection()

방향을 로컬에서 월드 기준으로 변환

transform.InverseTransformDirection()

월드 -> 로컬

transform.Translate

아래 같은 코드를 더 간편하게 변경

void Update()

{

if (Input.GetKey(KeyCode.W))

transform.position += transform.TransformDirection(Vector3.forward * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.S))

transform.position += transform.TransformDirection(Vector3.back * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.A)

) transform.position += transform.TransformDirection(Vector3.left * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.D))

transform.position += transform.TransformDirection(Vector3.right * Time.deltaTime * _speed);

}

이런 코드를

if (Input.GetKey(KeyCode.W))

transform.Translate(Vector3.forward * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.S))

transform.Translate(Vector3.back * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.A))

transform.Translate(Vector3.left * Time.deltaTime * _speed);

if (Input.GetKey(KeyCode.D))

transform.Translate(Vector3.right * Time.deltaTime * _speed);

짧게 만들어줌

방향 벡터

MyVec to = new MyVec(10,0,0);

MyVec from = new MyVec(5,0,0);

MyVec dir = to - from // 방향 벡터

방향벡터로

- 거리 (magnitude)
    
- 실제 방향
    

을 알 수 있음

transform.position.magnitude;

transform.position.normalized;

// 위치 벡터

// 방향 벡터

struct MyVector

{

public float x;

public float y;

public float z;

// 피타고라스

public float magnitude { get { return Mathf.Sqrt(x * x + y * y + z * z); } }

public MyVector normalized { get { return new MyVector(x / magnitude, y / magnitude, z / magnitude); } }

public MyVector(float x, float y, float z)

{

this.x = x;

this.y = y;

this.z = z;

}

public static MyVector operator +(MyVector a, MyVector b)

{

return new MyVector(a.x + b.x, a.y + b.y, a.z + b.z);

}

public static MyVector operator -(MyVector a, MyVector b)

{

return new MyVector(a.x - b.x, a.y - b.y, a.z - b.z);

}

public static MyVector operator *(MyVector a, float d)

{

return new MyVector(a.x * d, a.y * d, a.z * d);

}

}

transform.eulerAngles (잘 안씀 Rotate권장) -> const 값으로 뿅하고 업데이트 시켜주는 것

transform.Rotation(Vector3()) -> 현재 상태에 rotation vec3값을 더해주는 것

transform.rotation 은 Quaternion 타입으로 x,y,z,w 네 값을 가진다.

왜 이래야 하는지는

[https://www.youtube.com/watch?v=zc8b2Jo7mno](https://www.youtube.com/watch?v=zc8b2Jo7mno)



- Quaterniion 사용해서 회전 (주석)
- `Quaternion.LookRotation` 으로 캐릭터가 방향키 방향을 바라보도록 하기

```cs
using UnityEngine;



public class PlayerController : MonoBehaviour
{
    public float _speed = 10.0f;



    void Start()
    {

    }

    float _yAngle = 100;
    void Update()
    {
        _yAngle += Time.deltaTime * 100;

        // 절대 회전 값
        // transform.eulerAngles = new Vector3(0, _yAngle, 0);

        // 상대 회전 값 (누적)
        // transform.Rotate(new Vector3(0, Time.deltaTime * _yAngle, 0));

        // transform.rotation = Quaternion.Euler(new Vector3(0, _yAngle, 0));


        if (Input.GetKey(KeyCode.W))
        {
            transform.rotation = Quaternion.LookRotation(Vector3.forward);
            // transform.Translate(Vector3.forward * Time.deltaTime * _speed);
        }
        if (Input.GetKey(KeyCode.S))
        {
            transform.rotation = Quaternion.LookRotation(Vector3.back);
            // transform.Translate(Vector3.back * Time.deltaTime * _speed);
        }
        if (Input.GetKey(KeyCode.A))
        {
            transform.rotation = Quaternion.LookRotation(Vector3.left);
            //transform.Translate(Vector3.left * Time.deltaTime * _speed);
        }
        if (Input.GetKey(KeyCode.D))
        {
            transform.rotation = Quaternion.LookRotation(Vector3.right);
            // transform.Translate(Vector3.right * Time.deltaTime * _speed);
        }
    }
}
```

이렇게 하면 방향이 부드럽지 않게 변하기 때문에

`Quaternion.Slerp()` 사용해서 부드럽게 만들어준다

```cs
if (Input.GetKey(KeyCode.W))
{
    //transform.rotation = Quaternion.LookRotation(Vector3.forward);
    transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.forward), 1.0f);
    // transform.Translate(Vector3.forward * Time.deltaTime * _speed);
}
if (Input.GetKey(KeyCode.S))
{
    //transform.rotation = Quaternion.LookRotation(Vector3.back);
    transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.back), 1.0f);
    // transform.Translate(Vector3.back * Time.deltaTime * _speed);
}
if (Input.GetKey(KeyCode.A))
{
    //transform.rotation = Quaternion.LookRotation(Vector3.left);
    transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.left), 1.0f);
    //transform.Translate(Vector3.left * Time.deltaTime * _speed);
}
if (Input.GetKey(KeyCode.D))
{
    //transform.rotation = Quaternion.LookRotation(Vector3.right);
    transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.right), 1.0f);
    // transform.Translate(Vector3.right * Time.deltaTime * _speed);
}
```

두번째 파라미터 값이 `[0,1]` 값인데, 
0이면 안움직이고 1이면 기존 코드와 똑같이 동작함

그리고 나서 기존 이동 로직 방향을 모두 `Vector3.forward` 로 해주면 캐릭터가 바라보는 방향이 변하고, 그 방향으로 직진하는 코드가 완성됨

## Input Manager

키를 입력받아서 캐릭터를 움직이는 로직이 모두 `Update` 함수안에 박혀있다.

매 프레임마다 키 눌렀는지 체크하고 캐릭터 포지션과 로테이션 변경하면 낭비니까

이벤트로 처리한다

`Managers` 에서 InputMangaer의 인스턴스를 가지고 있을 것이기 때문에 `MonoBehavior`를 상속받을 필요는 없다.

```cs
// InputManager.cs
using System;
using UnityEngine;

public class InputManager
{
    public Action KeyAction = null;

   public void OnUpdate()
    {
        if (Input.anyKey == false) return;

        if (KeyAction != null) KeyAction.Invoke();
    }
}
```

```cs
// Managers.cs
using UnityEngine;

public class Managers : MonoBehaviour
{
    static Managers s_instance; // singleton pattern으로 유일성을 보장
    static Managers Instance { get { Init(); return s_instance; } }


    // Input Manager
    InputManager _input = new InputManager();
    public static InputManager Input { get { return Instance._input; } }

    void Start()
    {
        Init();
    }

    void Update()
    {
        _input.OnUpdate();
    }

    static void Init()
    {
        if (s_instance == null)
        {
            GameObject go = GameObject.Find("@Managers");
            if (go == null)
            {
                go = new GameObject { name = "@Managers" };
                go.AddComponent<Managers>();
            }

            DontDestroyOnLoad(go);

            s_instance = go.GetComponent<Managers>();
        }
    }
}

```

```cs
using UnityEngine;



public class PlayerController : MonoBehaviour
{
    public float _speed = 10.0f;



    void Start()
    {
        // 혹시라도 구독 돼있으면 해제하고 다시 등록
        Managers.Input.KeyAction += OnKeyboard;
        // Managers의 InputManager에 키보드 이벤트 등록
        Managers.Input.KeyAction += OnKeyboard;
    }

    void Update()
    {

       
    }

    void OnKeyboard()
    {
        // 절대 회전 값
        // transform.eulerAngles = new Vector3(0, _yAngle, 0);

        // 상대 회전 값 (누적)
        // transform.Rotate(new Vector3(0, Time.deltaTime * _yAngle, 0));

        // transform.rotation = Quaternion.Euler(new Vector3(0, _yAngle, 0));


        if (Input.GetKey(KeyCode.W))
        {
            //transform.rotation = Quaternion.LookRotation(Vector3.forward);
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.forward), 0.5f);
            transform.position += Vector3.forward * Time.deltaTime * _speed;
        }
        if (Input.GetKey(KeyCode.S))
        {
            //transform.rotation = Quaternion.LookRotation(Vector3.back);
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.back), 0.5f);
            transform.position += Vector3.back * Time.deltaTime * _speed;
        }
        if (Input.GetKey(KeyCode.A))
        {
            //transform.rotation = Quaternion.LookRotation(Vector3.left);
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.left), 0.5f);
            transform.position += Vector3.left * Time.deltaTime * _speed;
        }
        if (Input.GetKey(KeyCode.D))
        {
            //transform.rotation = Quaternion.LookRotation(Vector3.right);
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(Vector3.right), 0.5f);
            transform.position += Vector3.right * Time.deltaTime * _speed;
        }
    }
}

```

### `Instantiate()` 와 `Destroy()`

게임 오브젝트를 동적으로 생성하는 데 사용

```cs
// PrefabTest.cs
using UnityEngine;

public class PrefabTest : MonoBehaviour
{

    public GameObject prefab;

    void Start()
    {
        Instantiate(prefab);
    }
}
```

## ResourceManager

`Instantiate()`과 `Destroy()`  를 사용해서 ResourceManager를 만들기

```cs
// ResourceManager.cs
using UnityEngine;

public class ResourceManager
{
    public T Load<T>(string path) where T : Object
    {
        return Resources.Load<T>(path);
    }

    public GameObject Instantiate(string path, Transform parent = null)
    {
        GameObject prefab = Load<GameObject>($"Prefabs/{path}");
        if(prefab == null)
        {
            Debug.Log($"Failed to laod prefab : {path}");
            return null;
        }

        return Object.Instantiate(prefab, parent);
    }

    public void Destroy(GameObject gameObj)
    {
        if (gameObj == null) return;

        Object.Destroy(gameObj);
    }
}
```

## OnCollisionEnter, OnTriggerEnter

[Unity 5.3 Documentation - Event Functions ](https://docs.unity3d.com/kr/530/Manual/EventFunctions.html) Physics events 참고
[Unity - Collider overview](https://docs.unity3d.com/kr/current/Manual/CollidersOverview.html)
[Unity - Interaction between collider types](https://docs.unity3d.com/kr/current/Manual/collider-types-interaction.html)

### Collision

[Unity - Collision](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Collision.html)



### Trigger


## Raycasting

```cs
// TestCollision.cs
using UnityEngine;

public class TestCollision : MonoBehaviour
{
    //private void OnCollisionEnter(Collision collision)
    //{
    //    Debug.Log($"Collision {collision.gameObject.name}");
    //}

    //private void OnTriggerEnter(Collider other)
    //{
    //    Debug.Log($"Trigger {other.gameObject.name}");
    //}


    void Start()
    {

    }

    void Update()
    {
        Vector3 playerLook = transform.TransformDirection(Vector3.forward);
        Debug.DrawRay(transform.position + Vector3.up, playerLook * 10, Color.red);

        RaycastHit hit;

        if (Physics.Raycast(transform.position, playerLook, out hit, 10))
        {
            Debug.Log($"Raycast {hit.collider.gameObject.name}");
        }
    }
}
```

player가 바라보는