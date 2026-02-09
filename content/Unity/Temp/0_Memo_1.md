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

player가 바라보는 방향으로 Raycast 하기 위해  `transform.TransformDirection()` 을 사용

`Raycast` 함수는 기본적으로 hit된 모든 오브젝트가 아니라 가장 처음으로 hit 되는 오브젝트가 된다.
Ray 상 모든 오브젝트 정보를 알고 싶으면 RaycastAll 을 사용한다.

```cs
RaycastHit[] hits;
hits = Physics.RaycastAll(transform.position + Vector3.up, look, 10);
```

## 투영의 개념

### 마우스 포인터 위치 찾아보기

```cs
void Update()
{
    Debug.Log(Input.mousePosition); // 스크린 좌표

    Debug.Log(Camera.main.ScreenToViewportPoint(Input.mousePosition)); // 뷰포트 좌표
}
```

스크린 좌표는 말그대로 스크린 안에서의 좌표이다. 0,0부터 최대 스크린의 width,height 까지 값을 얻을 수 있다.

`Input.mousePosition`을 `Camera.main.ScreenToViewportPoint()` 로 뷰포트 좌표로 변환해 볼 수 있다.

Screen space가 픽셀로 정의된 데에 비해 Viewport space는 최대가 1,1인 정규화된 값을 갖는다.

### 클릭한 곳의 글로벌 좌표 찾아보기

```cs
 void Update()
 {
     //Debug.Log(Input.mousePosition); // 스크린 좌표

     //Debug.Log(Camera.main.ScreenToViewportPoint(Input.mousePosition)); // 뷰포트 좌표

     if (Input.GetMouseButtonDown(0))
     {
         Vector3 mousePos = Camera.main.ScreenToWorldPoint(new Vector3(Input.mousePosition.x, Input.mousePosition.y, Camera.main.nearClipPlane));
         Vector3 dir = mousePos - Camera.main.transform.position;
         dir = dir.normalized;

         Debug.DrawRay(Camera.main.transform.position, dir, Color.red, 1.0f);

         RaycastHit hit;
         if (Physics.Raycast(Camera.main.transform.position, dir, out hit))
         {
             Debug.Log($"Raycast Camera {hit.collider.gameObject.name}");
         }
     }
 }
```

번거롭게 마우스 포지션을 월드 좌표로 변환하고, 방향을 알아내고, 해당 방향으로 Ray를 쏴서 어떤 오브젝트가 맞았는지 확인하는 과정이 번거롭다.

`Ray` 를사용하면 이 코드를 획기적으로 줄여준다.

```cs
 void Update()
 {
     //Debug.Log(Input.mousePosition); // 스크린 좌표

     //Debug.Log(Camera.main.ScreenToViewportPoint(Input.mousePosition)); // 뷰포트 좌표

     if (Input.GetMouseButtonDown(0))
     {
         Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

         Debug.DrawRay(Camera.main.transform.position, ray.direction, Color.red, 1.0f);

         RaycastHit hit;
         
         if (Physics.Raycast(ray, out hit, 100))
         {
             Debug.Log($"Raycast Camera {hit.collider.gameObject.name}");
         }
     }
 }
```

## LayerMask

Raycasting의 성능과 최적화에 관하여
Ray에 부딪히는 오브젝트가 많아짐에 따라 성능 문제가 발생할 수 있다.

**Layer** 기능을 사용하면 필요한 부분만 선택적으로 Ray 연산할 수 있다.

[HardCore in Programming - Physics.Raycast 완벽 가이드](https://kukuta.tistory.com/391)

![[‎Tuesday‎,_‎February‎_‎10‎,_‎2026.png]]
![[Pasted image 20260210012955.png]]

Builtin 레이어를 포함하여 총 32개의 레이어가 존재한다.

32bit 정수를 `Raycast` 함수의 파라미터로 넘겨줘서 어떤 Layer에 대해 Raycast를 적용할지 정할 수 있다.

```cs
public static bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance, int layerMask);
```

오버로드된 `Raycast`함수들 중 위 버전을 사용하면 layerMask를 bit 마스킹 한 int 값으로 넘겨줄 수 있다.

```cs
if (Input.GetMouseButtonDown(0))
{
    Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

    Debug.DrawRay(Camera.main.transform.position, ray.direction, Color.red, 1.0f);

    RaycastHit hit;

    int layerMask = 1 << 7; // 7번째 비트 on
    
    if (Physics.Raycast(ray, out hit, 100, layerMask))
    {
        Debug.Log($"Raycast Camera {hit.collider.gameObject.name}");
    }
}
```

이러면 7번째 레이어만 hit 한다.

반대로 `~(1 << 7)`은 7번째 빼고 모두를 1로 만든다.

`(1 << 7) | (1 << 3)` 은 7번째와 3번째 비트를 1로 만든다.

```cs
if (Input.GetMouseButtonDown(0))
{
    Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

    Debug.DrawRay(Camera.main.transform.position, ray.direction, Color.red, 1.0f);

    RaycastHit hit;

	LayerMask layerMask = LayerMask.GetMask("Monster");
    
    if (Physics.Raycast(ray, out hit, 100, layerMask))
    {
        Debug.Log($"Raycast Camera {hit.collider.gameObject.name}");
    }
}

```

`LayerMask` 라는 객체를 사용하여 설정한 레이어 이름으로 마스크를 가져올 수도 있다.

## Tag

Layer 뿐만 아니라 Tag라는 것도 있는데,

Tag를 이용하여 GameObject를 찾는 기능이 있다.

`GameObject.FindGameObjectWithTag("Monster")` 

