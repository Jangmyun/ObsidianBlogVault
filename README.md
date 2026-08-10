# Jangmyun's Vault

개발 공부와 프로젝트 기록을 정리하는 개인 Obsidian 노트 저장소입니다. [Quartz](https://quartz.jzhao.xyz/) 로 빌드되어 정적 사이트로 배포됩니다.

🔗 **https://blog.jangmyun.dev**

## 다루는 주제

- Programming Language (C++, C#, PLT)
- Computer Network / Security / Vision / Graphics
- Operating System / Database
- 진행한 프로젝트 기록

## 로컬에서 빌드하기

```bash
npm install
npx quartz build --serve
```

## 스택

Obsidian 으로 작성한 마크다운 노트(`content/`)를 Quartz 4로 빌드해 Cloudflare Pages에 배포합니다.

## 이미지 업로드

첨부 이미지는 저장소에 커밋하지 않고 Nextcloud(`cloud.jangmyun.dev`)에 올려서 공유 링크로 참조합니다.

**최초 1회 설정:**

```bash
cp scripts/.nextcloud-credentials.example .nextcloud-credentials
# .nextcloud-credentials 열어서 NEXTCLOUD_APP_PASSWORD 채우기
# (Nextcloud 웹 UI: 설정 > 보안 > 새 앱 비밀번호 생성, 계정 로그인 비밀번호 아님)
```

**평소 작업 흐름:**

1. Obsidian에서 평소처럼 스크린샷 붙여넣기 (`![[파일명]]`로 임베드됨)
2. 글 다 쓰면:
   ```bash
   python3 scripts/sync-images.py         # 실제 업로드+링크교체+로컬삭제
   python3 scripts/sync-images.py --dry-run  # 미리보기만, 아무것도 안 바꿈
   ```
3. `git diff`로 확인 후 커밋 & 푸시

이미 업로드된 이미지(공유 링크로 바뀐 것)는 다시 실행해도 건드리지 않습니다.
