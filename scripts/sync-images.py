#!/usr/bin/env python3
"""
Upload newly-pasted Obsidian images to Nextcloud and rewrite the
![[filename]] embeds in content/*.md into public share links.

Usage:
    python3 scripts/sync-images.py [--dry-run]

Setup (one-time, per machine):
    cp scripts/.nextcloud-credentials.example .nextcloud-credentials
    # then fill in .nextcloud-credentials with real values (gitignored)
"""
import base64
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(VAULT_ROOT, "content")
CREDS_PATH = os.path.join(VAULT_ROOT, ".nextcloud-credentials")

IMAGE_EXTS = ("png", "jpg", "jpeg", "gif", "webp", "svg")
WIKILINK_RE = re.compile(
    r"!\[\[([^\]|]+\.(?:" + "|".join(IMAGE_EXTS) + r"))\]\]", re.IGNORECASE
)

DRY_RUN = "--dry-run" in sys.argv


def load_credentials():
    if not os.path.isfile(CREDS_PATH):
        sys.exit(
            f"credentials file not found: {CREDS_PATH}\n"
            f"copy scripts/.nextcloud-credentials.example to .nextcloud-credentials "
            f"and fill it in first."
        )
    creds = {}
    with open(CREDS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()
    required = ["NEXTCLOUD_BASE_URL", "NEXTCLOUD_USER", "NEXTCLOUD_APP_PASSWORD",
                "NEXTCLOUD_REMOTE_FOLDER", "NEXTCLOUD_SHARE_TOKEN"]
    missing = [k for k in required if not creds.get(k)]
    if missing:
        sys.exit(f"missing keys in {CREDS_PATH}: {', '.join(missing)}")
    return creds


def find_local_file(filename):
    """Obsidian resolves ![[name]] by filename regardless of subfolder."""
    for root, _dirs, files in os.walk(CONTENT_DIR):
        if filename in files:
            return os.path.join(root, filename)
    return None


def webdav_exists(creds, filename):
    url = (
        f"{creds['NEXTCLOUD_BASE_URL']}/remote.php/dav/files/"
        f"{creds['NEXTCLOUD_USER']}/{creds['NEXTCLOUD_REMOTE_FOLDER']}/"
        f"{urllib.parse.quote(filename)}"
    )
    req = urllib.request.Request(url, method="HEAD")
    _add_auth(req, creds)
    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def webdav_put(creds, local_path, filename):
    url = (
        f"{creds['NEXTCLOUD_BASE_URL']}/remote.php/dav/files/"
        f"{creds['NEXTCLOUD_USER']}/{creds['NEXTCLOUD_REMOTE_FOLDER']}/"
        f"{urllib.parse.quote(filename)}"
    )
    with open(local_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(url, data=data, method="PUT")
    _add_auth(req, creds)
    req.add_header("Content-Type", "application/octet-stream")
    urllib.request.urlopen(req)


def _add_auth(req, creds):
    token = base64.b64encode(
        f"{creds['NEXTCLOUD_USER']}:{creds['NEXTCLOUD_APP_PASSWORD']}".encode()
    ).decode()
    req.add_header("Authorization", f"Basic {token}")
    # Cloudflare blocks the default Python-urllib User-Agent as bot traffic.
    req.add_header("User-Agent", "ObsidianBlogVault-sync/1.0")


def share_url(creds, filename):
    base = f"{creds['NEXTCLOUD_BASE_URL']}/s/{creds['NEXTCLOUD_SHARE_TOKEN']}/download"
    encoded = urllib.parse.quote(filename)
    return f"{base}?path=%2F&files={encoded}"


def main():
    creds = load_credentials()

    md_files = []
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for fn in files:
            if fn.endswith(".md"):
                md_files.append(os.path.join(root, fn))

    uploaded, skipped, missing, errors = [], [], [], []

    for path in md_files:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        matches = list(WIKILINK_RE.finditer(content))
        if not matches:
            continue

        new_content = content
        changed = False

        for m in matches:
            filename = m.group(1)
            local_path = find_local_file(filename)
            if local_path is None:
                missing.append((path, filename))
                continue

            try:
                already_remote = webdav_exists(creds, filename)
            except Exception as e:
                errors.append((filename, f"exists-check failed: {e}"))
                continue

            if not already_remote:
                if DRY_RUN:
                    print(f"[dry-run] would upload {filename}")
                else:
                    try:
                        webdav_put(creds, local_path, filename)
                    except Exception as e:
                        errors.append((filename, f"upload failed: {e}"))
                        continue
                    uploaded.append(filename)
            else:
                skipped.append(filename)

            alt = os.path.splitext(filename)[0]
            url = share_url(creds, filename)
            new_content = new_content.replace(
                m.group(0), f"![{alt}]({url})"
            )
            changed = True

            if not DRY_RUN:
                try:
                    os.remove(local_path)
                except OSError:
                    pass

        if changed and not DRY_RUN:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

    print()
    print(f"업로드: {len(uploaded)}  이미 있음(링크만 교체): {len(skipped)}  "
          f"파일 못 찾음: {len(missing)}  에러: {len(errors)}")
    if missing:
        print("\n로컬에서 못 찾은 파일 (vault 어디에도 없음):")
        for path, fn in missing:
            print(f"  {os.path.relpath(path, VAULT_ROOT)} -> {fn}")
    if errors:
        print("\n에러:")
        for fn, err in errors:
            print(f"  {fn}: {err}")
    if DRY_RUN:
        print("\n(--dry-run: 실제 업로드/삭제/수정은 안 했습니다)")


if __name__ == "__main__":
    main()
