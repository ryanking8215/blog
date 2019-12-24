---
title: 用户认证加密方法
date: 2014-10-05T17:20:36+08:00
categories: ["Tech"]
tags: ["encrypto"]
slug: user-encrypto
keywords:
  - encryption
  - 加密
  - 密码
  - password
description: 用户密码加密方法
---

## 简单方法
		sha256(sha256(passwd) + passwd_salt)

passwd_salt 是一个随机生成的 sha256 值。
salt和key都要存储

## 标准方法 
[PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)
[BCRYPT] (https://en.wikipedia.org/wiki/Bcrypt)