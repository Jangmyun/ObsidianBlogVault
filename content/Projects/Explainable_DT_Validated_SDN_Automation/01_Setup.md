---
title: 01 - 프로젝트 셋업과 스택
description:
draft: false
tags:
  - Project
---
# 1. 환경

- Arch Linux 7.0.14
- ARM64 Ubuntu 24.04 (UTM 사용)

```bash
sudo apt update
sudo apt upgrade -y
```

### Mininet, OVS, iperf3 설치

```bash
sudo apt install 0y mininet openvswitch-switch iperf3
```

```bash
mn --version # 2.3.0
ovs-vsctl --version # 3.3.4
iperf3 --version # 3.16
```

### uv 를 통한 프로젝트 관리

```bash
sudo apt install -y curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
source ~/.bashrc

uv --version
```

### ONOS

openjdk17 설치

```bash
sudo apt install -y openjdk-17-jdk
```

[Docker 설치](https://docs.docker.com/engine/install/)

```bash
sudo systemctl enable docker
sudo usermod -aG docker $USER
reboot
```

ONOS 컨테이너 실행 테스트

```bash

```

