title: 用户加密方法
categories: tech
date: 2014-10-05 17:20:36
tags:
---

## 简单方法
		sha256(sha256(passwd) + passwd_salt)

passwd_salt 是一个随机生成的 sha256 值。
salt和key都要存储

## 标准方法 
[PBKDF2](http://en.wikipedia.org/wiki/PBKDF2)