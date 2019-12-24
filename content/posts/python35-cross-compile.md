---
title: python3.5 交叉编译
date: 2016-01-17T14:50:54+08:00
categories: ["Tech"]
tags: ["python", "cross-compile"]
slug: python35-cross-compile
keywords:
  - python
  - python3
  - cross compile
  - 交叉编译
  - embedded system
  - 嵌入式系统
description: 交叉编译python3.5.1的方法, 用于嵌入式系统。
---

有一个嵌入式项目，尝试将python3.5.1移植到该平台。还未确定是否用python开发, 先把
环境整好，到时想用就能用了，也记录一下，可以用这种方法移植到其他平台。

# 问题
Python工程本来就有`configure`工具，理论上讲交叉编译比较简单，只要指定`--host`为你
的交叉编译工具链即可。其他基于`autoconf/automake`的也是类似的。但是Python比较特殊
的是，在交叉编译过程中，会生成`Parse/Pgen`和`python`应用程序，然后会运行该程序,
那么问题来了，交叉编译出来的程序在开发机上无法执行的，它们是运行在嵌入式系统上的。

查看网络上的解决方法:

- 为Python工程打补丁

	打补丁的方法只支持到3.2，新版本就没有了, 大意是先是用本地的编译器编译出python和pgen，改名，然后再是用
	交叉编译工具编译，当然需要加入特殊的命令行参数来指定刚才编译出来的python和pgen。
	
- 压根不处理

	不处理的也有，就直接make就ok了，是python3.4+mips的环境，不明白怎么没碰到这个问题。


看来要自己解决了。
尝试忽略执行该程序的过程，修改`Makefile`, 找到这部分，把它们注释掉，
继续make，最后ok了。
可能不是一个好方法，但是一个可行的方法。

# 参考
网上找了很多资料做参考，这里记录一下。

- [交叉编译Python至嵌入式arm(支持import sqlite3,datetime等)-----Cross Compiling Python for Emb...](http://www.tuicool.com/articles/b6f6Nvf)
- [交叉编译Python 3.3 压成1.5MB](http://www.tuicool.com/articles/YRFFfa)
- [为 Kindle 交叉编译 Zsh 和 Python 3.3](http://www.tuicool.com/articles/qe6V3y)
