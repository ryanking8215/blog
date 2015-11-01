Title: 用户加密方法
Date: 2014-10-05 17:20:36
Category: Tech
Tags: encrypto
Slug: user-encrypto
Summary:

## 简单方法
		sha256(sha256(passwd) + passwd_salt)

passwd_salt 是一个随机生成的 sha256 值。
salt和key都要存储

## 标准方法 
[PBKDF2](http://en.wikipedia.org/wiki/PBKDF2)