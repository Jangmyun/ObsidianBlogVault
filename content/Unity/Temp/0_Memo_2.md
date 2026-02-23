---
title: Example Title
description: Example Description
draft: true
tags:
  - Unity
---

## 카메라와 캐릭터 사이에 장애물 있을 때 카메라 이동 로직

```cs
using UnityEngine;

public class CameraController : MonoBehaviour
{


    [SerializeField] Define.CameraMode _mode = Define.CameraMode.QuaterView; // ī�޶� ���
    [SerializeField] Vector3 _delta = new Vector3(0, 6, -5); // ī�޶�� Ÿ�ٰ��� �Ÿ�
    [SerializeField] GameObject _player; // ī�޶� ����ٴ� Ÿ�� ������Ʈ

    void Start()
    {

    }

    void LateUpdate()
    {
        if (_mode == Define.CameraMode.QuaterView)
        {
            RaycastHit hit;
            if (Physics.Raycast(_player.transform.position, _delta, out hit, _delta.magnitude, LayerMask.GetMask("Wall")))
            {
                float distance = (hit.point - _player.transform.position).magnitude * 0.8f;
                transform.position = _player.transform.position + _delta.normalized * distance;
            }
            else
            {
                transform.position = _player.transform.position + _delta;
                transform.LookAt(_player.transform);
            }


        }

    }

    public void SetQuaterView(Vector3 delta)
    {
        _mode = Define.CameraMode.QuaterView;
        _delta = delta;
    }

}

```


# Animation 기초

## State 패턴

```cs
// PlayerController.cs

using System;
using UnityEngine;



public class PlayerController : MonoBehaviour
{
    public float _speed = 10.0f;

    Vector3 _destPos; // �̵��� ������ ��ǥ


    void Start()
    {
        // Mouse Event ���
        Managers.Input.MouseAction -= OnMouseClicked;
        Managers.Input.MouseAction += OnMouseClicked;

    }

    float wait_run_ratio = 0f;

    public enum PlayerState
    {
        Die,
        Moving,
        Idle
    }

    PlayerState _state = PlayerState.Idle;

    void UpdateDie()
    {

    }

    void UpdateMoving()
    {
        Vector3 dir = _destPos - transform.position;
        if (dir.magnitude < 0.001)
        {
            _state = PlayerState.Idle;
        }
        else
        {
            float moveDist = Math.Clamp(_speed * Time.deltaTime, 0, dir.magnitude);
            transform.position += dir.normalized * moveDist;

            // LookRotation 사용하여 부드럽게 만들기
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(dir), 10 * Time.deltaTime);
        }

        // Animation
        Animator animator = GetComponent<Animator>();
        wait_run_ratio = Mathf.Lerp(wait_run_ratio, 1, 10.0f * Time.deltaTime);
        animator.SetFloat("wait_run_ratio", wait_run_ratio);
        animator.Play("WAIT_RUN");
    }

    void UpdateIdle()
    {
        Animator animator = GetComponent<Animator>();
        wait_run_ratio = Mathf.Lerp(wait_run_ratio, 0, 10.0f * Time.deltaTime);
        animator.SetFloat("wait_run_ratio", wait_run_ratio);
        animator.Play("WAIT_RUN");
    }

    void Update()
    {
        switch (_state)
        {
            case PlayerState.Die:
                UpdateDie();
                break;
            case PlayerState.Moving:
                UpdateMoving();
                break;
            case PlayerState.Idle:
                UpdateIdle();
                break;
        }
    }


    // ���ڰ� Define.MouseEvent�� Action�̹Ƿ� �Ķ���� �߰�
    void OnMouseClicked(Define.MouseEvent evt)
    {
        if (_state == PlayerState.Die) return;

        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

        Debug.DrawRay(Camera.main.transform.position, ray.direction, Color.red, 1.0f);

        RaycastHit hit;

        int layerMask = 1 << 7; // Wall Layer Masking


        if (Physics.Raycast(ray, out hit, 100, layerMask: layerMask))
        {
            // Debug.Log($"Raycast Camera {hit.collider.gameObject.name}");
            _destPos = hit.point;
            _state = PlayerState.Moving;
        }

    }
}

```


Animation Controller 에 파라미터를 추가하고 변경하는 것도 가능하다

```cs
// PlayerController.cs

void UpdateMoving()
    {
        Vector3 dir = _destPos - transform.position;
        if (dir.magnitude < 0.001)
        {
            _state = PlayerState.Idle;
        }
        else
        {
            float moveDist = Math.Clamp(_speed * Time.deltaTime, 0, dir.magnitude);
            transform.position += dir.normalized * moveDist;

            // LookRotation 사용하여 부드럽게 만들기
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(dir), 10 * Time.deltaTime);
        }

        // Animation
        Animator animator = GetComponent<Animator>();
        // wait_run_ratio = Mathf.Lerp(wait_run_ratio, 1, 10.0f * Time.deltaTime);
        // animator.SetFloat("wait_run_ratio", wait_run_ratio);
        // animator.Play("WAIT_RUN");
        animator.SetFloat("speed", _speed);
    }

    void UpdateIdle()
    {
        Animator animator = GetComponent<Animator>();
        // wait_run_ratio = Mathf.Lerp(wait_run_ratio, 0, 10.0f * Time.deltaTime);
        // animator.SetFloat("wait_run_ratio", wait_run_ratio);
        // animator.Play("WAIT_RUN");
        animator.SetFloat("speed", 0);
    }
```


## UI

### 게임오브젝트와 UI 클릭 시 구분

```cs
public void OnUpdate()
    {

        // UI 버튼이 클릭 됐는지 여부를 판단
        if (EventSystem.current.IsPointerOverGameObject()) return;


        if (Input.anyKey && KeyAction != null) KeyAction.Invoke();

        if (Input.GetMouseButton(0)) // 0: ����, 1: ������, 2: �� Ŭ��
        {
            MouseAction.Invoke(Define.MouseEvent.Press);
            _pressed = true;
        }
        else
        {
            if (_pressed)
            {
                MouseAction.Invoke(Define.MouseEvent.Click);
            }
            _pressed = false;
        }

    }
```

### Button 클릭 시 Text 변경
```cs
using TMPro;
using UnityEngine;

public class UI_Button : MonoBehaviour
{
    [SerializeField] TMP_Text _text;
    private int _score = 0;

    void OnButtonClicked()
    {
        _score++;
        _text.text = $"Score: {_score}";
    }
}

```

## UI 자동화

reflection을 사용하여 존재하는 object 에 대한 정보를 추출하여 UI에 이벤트 함수를 넣을 수 있도록 한다.

```cs
// TestUI_Button
using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class UI_Button : MonoBehaviour
{
    // Type에 딸린 UnityEngine이 모두 상속받는 Object배열을 선언
    Dictionary<Type, UnityEngine.Object[]> _objects = new Dictionary<Type, UnityEngine.Object[]>();

    enum Buttons
    {
        PointButton,
    }

    enum Texts
    {
        PointText,
        ScoreText
    }

    void Bind<T>(Type type)
    {
        string[] names = Enum.GetNames(type); // Enum 에서 상수 이름의 배열을 검색하여 저장


        UnityEngine.Object[] objects = new UnityEngine.Object[names.Length]; // 상수 이름 배열 길이만큼 Object 배열 생성
        _objects.Add(typeof(T), objects); // Dictionary에 저장

        for (int i = 0; i < names.Length; ++i)
        {
            objects[i] = null;
        }
    }

    void Start()
    {
        Bind<Button>(typeof(Buttons));
        Bind<TMP_Text>(typeof(Texts));
    }

    [SerializeField] TMP_Text _text;
    private int _score = 0;

    void OnButtonClicked()
    {
        _score++;
        _text.text = $"Score: {_score}";
    }

}

```

GameObject에서 하위에 같은 이름의 자식이 있는지 조회하는 기능을 Utils에 따로 만들어본다


```cs
// objects[i] = null;
objects[i] = Utils.FindChild<T>(gameObject, names[i], true);
```


```cs
// Utils
using UnityEngine;

public class Utils
{
    public static T FindChild<T>(GameObject go, string name = null, bool recursive = false) where T : UnityEngine.Object
    {
        if (go == null) return null;

        if (!recursive)
        {
            for (int i = 0; i < go.transform.childCount; ++i)
            {
                Transform childTransform = go.transform.GetChild(i);
                if (string.IsNullOrEmpty(name) || childTransform.name == name)
                {
                    T component = childTransform.GetComponent<T>();
                    if (component != null) return component;
                }
            }
        }
        else
        {
            foreach (T component in go.GetComponentsInChildren<T>())
            {
                if (string.IsNullOrEmpty(name) || component.name == name) return component;
            }
        }

        return null;
    }
}
```

UI object 를 get 하는 함수도 만든다.

```cs

    void Bind<T>(Type type) where T : UnityEngine.Object
    {
        string[] names = Enum.GetNames(type); // Enum 에서 상수 이름의 배열을 검색하여 저장


        UnityEngine.Object[] objects = new UnityEngine.Object[names.Length]; // 상수 이름 배열 길이만큼 Object 배열 생성
        _objects.Add(typeof(T), objects); // Dictionary에 저장

        for (int i = 0; i < names.Length; ++i)
        {
            objects[i] = Utils.FindChild<T>(gameObject, names[i], true);
        }
    }

    T Get<T>(int idx) where T : UnityEngine.Object
    {
        UnityEngine.Object[] objects = null;
        if (_objects.TryGetValue(typeof(T), out objects) == false) return null;

        return objects[idx] as T;
    }
```


### 전체 결과물

임시 파일에 작성하던 것을 상속받아 사용할 수 있는 `UI_Base.cs` 스크립트로 만ㄷ

```cs
// UI_Base.cs
using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
public class UI_Base : MonoBehaviour
{
    Dictionary<Type, UnityEngine.Object[]> _objects = new Dictionary<Type, UnityEngine.Object[]>();

    protected void Bind<T>(Type type) where T : UnityEngine.Object
    {
        string[] names = Enum.GetNames(type); // Enum 에서 상수 이름의 배열을 검색하여 저장

        UnityEngine.Object[] objects = new UnityEngine.Object[names.Length]; // 상수 이름 배열 길이만큼 Object 배열 생성
        _objects.Add(typeof(T), objects); // Dictionary에 저장

        for (int i = 0; i < names.Length; ++i)
        {
            if (typeof(T) == typeof(GameObject))
                objects[i] = Utils.FindChild(gameObject, names[i], true);
            else
                objects[i] = Utils.FindChild<T>(gameObject, names[i], true);

            if (objects[i] == null) Debug.Log($"Failed to bind {names[i]}");
        }
    }

    protected T Get<T>(int idx) where T : UnityEngine.Object
    {
        UnityEngine.Object[] objects = null;
        if (_objects.TryGetValue(typeof(T), out objects) == false) return null;

        return objects[idx] as T;
    }

    protected TMP_Text GetTMP_Text(int idx) { return Get<TMP_Text>(idx); }
    protected Button GetButton(int idx) { return Get<Button>(idx); }
    protected Image GetImage(int idx) { return Get<Image>(idx); }
}
```

상속받은 자식 클래스도 메서드를 사용할 수 있어야 하기 때문에 protected 로 설정해준다.

```cs
// UI_Button.cs
using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class UI_Button : UI_Base
{


    enum Buttons
    {
        PointButton,
    }

    enum Texts
    {
        PointText,
        ScoreText
    }

    enum GameObjects
    {
        TestObject
    }

    void Start()
    {
        Bind<Button>(typeof(Buttons));
        Bind<TMP_Text>(typeof(Texts));
        Bind<GameObject>(typeof(GameObjects));

        GetTMP_Text((int)Texts.ScoreText).text = "Bind Test";
    }

    [SerializeField] TMP_Text _text;
    private int _score = 0;

    void OnButtonClicked()
    {
        _score++;
    }

}

```


## UI Event Handler 드래그 처리

```cs
// UI_EventHandler

using UnityEngine;
using UnityEngine.EventSystems;

public class UI_EventHandler : MonoBehaviour, IBeginDragHandler, IDragHandler
{
    public void OnBeginDrag(PointerEventData eventData)
    {
        Debug.Log("OnBeginDrag");
    }

    public void OnDrag(PointerEventData eventData)
    {
        Debug.Log("OnDrag");
        transform.position = eventData.position;
    }
}

```

`IBeginDragHandler`, `IDragHandler` 인터페이스를 구현하면 drag가 가능

## AddUIEvent 처리

```cs
// UI_Base.cs
using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
public class UI_Base : MonoBehaviour
{
    Dictionary<Type, UnityEngine.Object[]> _objects = new Dictionary<Type, UnityEngine.Object[]>();

    protected void Bind<T>(Type type) where T : UnityEngine.Object
    {
        string[] names = Enum.GetNames(type); // Enum 에서 상수 이름의 배열을 검색하여 저장

        UnityEngine.Object[] objects = new UnityEngine.Object[names.Length]; // 상수 이름 배열 길이만큼 Object 배열 생성
        _objects.Add(typeof(T), objects); // Dictionary에 저장

        for (int i = 0; i < names.Length; ++i)
        {
            if (typeof(T) == typeof(GameObject))
                objects[i] = Utils.FindChild(gameObject, names[i], true);
            else
                objects[i] = Utils.FindChild<T>(gameObject, names[i], true);

            if (objects[i] == null) Debug.Log($"Failed to bind {names[i]}");
        }
    }

    protected T Get<T>(int idx) where T : UnityEngine.Object
    {
        UnityEngine.Object[] objects = null;
        if (_objects.TryGetValue(typeof(T), out objects) == false) return null;

        return objects[idx] as T;
    }

    protected TMP_Text GetTMP_Text(int idx) { return Get<TMP_Text>(idx); }
    protected Button GetButton(int idx) { return Get<Button>(idx); }
    protected Image GetImage(int idx) { return Get<Image>(idx); }

    public static void AddUIEvent(GameObject go, Action<PointerEventData> action, Define.UIEvent type = Define.UIEvent.Click)
    {
        UI_EventHandler eventHandler = Utils.GetOrAddComponent<UI_EventHandler>(go);

        switch (type)
        {
            case Define.UIEvent.Click:
                eventHandler.OnClickHandler -= action;
                eventHandler.OnClickHandler += action;
                break;
            case Define.UIEvent.Drag:
                eventHandler.OnDragHandler -= action;
                eventHandler.OnDragHandler += action;
                break;
        }
    }
}

```

```cs
// UI_EventHandler.cs
using System;
using UnityEngine;
using UnityEngine.EventSystems;

public class UI_EventHandler : MonoBehaviour, IDragHandler, IPointerClickHandler
{
    public Action<PointerEventData> OnClickHandler = null;
    public Action<PointerEventData> OnDragHandler = null;

    public void OnPointerClick(PointerEventData eventData)
    {
        if (OnClickHandler != null) OnClickHandler.Invoke(eventData);
    }



    public void OnDrag(PointerEventData eventData)
    {
        // Debug.Log("OnDrag");
        // transform.position = eventData.position;

        if (OnDragHandler != null) OnDragHandler.Invoke(eventData);
    }


}

```

```cs
// Utils.cs

public class Utils
{
    public static T GetOrAddComponent<T>(GameObject go) where T : UnityEngine.Component
    {
        T component = go.GetComponent<T>();
        if (component == null) component = go.AddComponent<T>();

        return component;
    }
}
```

이제 `AddUIEvent` 함수를 통해 편리하게 gameobject에 추가하고싶은 Action을 추가할 수 있다.

```cs
// UI_Button : UI_Base

    void Start()
    {
        Bind<Button>(typeof(Buttons));
        Bind<TMP_Text>(typeof(Texts));
        Bind<GameObject>(typeof(GameObjects));
        Bind<Image>(typeof(Images));

        GetTMP_Text((int)Texts.ScoreText).text = "Bind Test";

        GameObject go = GetImage((int)Images.ItemIcon).gameObject;

		// Action 추가
        AddUIEvent(go, (PointerEventData data) => { go.transform.position = data.position; }, Define.UIEvent.Drag);
    }
```

### Extension Method

위에서 만든 편리한 함수들을 GameObject 객체 자체의 메서드로 사용가능하게 만들 수 있다.

```cs
// Utils/Extension.cs
using System;
using UnityEngine;
using UnityEngine.EventSystems;

public static class Extension
{
    public static void AddUIEvent(this GameObject go, Action<PointerEventData> action, Define.UIEvent type = Define.UIEvent.Click)
    {
        UI_Base.AddUIEvent(go, action, type);
    }
}

```

기존 `AddUIEvent` 함수 원형에 GameObject 파라미터에 `this`를 붙이게 되면 바로 사용 가능하다

```cs
// UI_Button.cs
    void Start()
    {
        Bind<Button>(typeof(Buttons));
        Bind<TMP_Text>(typeof(Texts));
        Bind<GameObject>(typeof(GameObjects));
        Bind<Image>(typeof(Images));

        GetButton((int)Buttons.PointButton).gameObject.AddUIEvent(OnButtonClicked);

        GameObject go = GetImage((int)Images.ItemIcon).gameObject;
        AddUIEvent(go, (PointerEventData data) => { go.transform.position = data.position; }, Define.UIEvent.Drag);
    }

```

## UI Manager

팝업되는 UI canvas의 sort order 관리

팝업되는 UI인지 아닌지를 구분해야 함

ui 프리팹 폴더 하위에 UI_Popup, UI_Scene 폴더를 만들어 구분해주고, UI 스크립트 에도 동일한 이름 폴더를 만든다.

하위에 각각 `UI_Popup.cs`, `UI_Scene.cs` 스크립트를 각각 만들어주고, `Monobehaviour` 가 아니라 `UI_Base` 를 상속받아준다.
