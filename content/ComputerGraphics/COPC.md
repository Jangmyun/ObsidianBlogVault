---
title: Example Title
description: Example Description
draft: true
tags:
  - computer_graphics
  - copc
---
 
# COPC (Cloud Optimized Point Cloud)

클러스터링된 옥트리 (octree) 구조로 데이터를 저장하는 LAZ 1.4 파일이다.
옥트리 구조를 기술하는 VLR (Variable Length Record) 를 포함하고, 실제 데이터는 LAZ 1.4 청크 형태로 저장된다.

![[Pasted image 20260623182038.png]]

## Octree

[참고자료- Octree(옥트리)](https://blog.naver.com/hermet/57456541)

3차원 공간을 8개의 자식 노드로 재귀적으로 분할하는 트리구조이다.

Level 0는 전체 공간을 1개 노드로 
