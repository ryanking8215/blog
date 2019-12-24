---
title: pjsip的一些问题
date: 2013-06-05T17:20:00+08:00
categories: ["Tech"]
tags: ["linux", "c"]
slug: pjsip-stuff
keywords:
  - pjsip
  - linux
  - c
description: pjsip使用过程中总结的问题，不定时更新...
---

## 多线程
多线程调用pjlib的api需要注册进pjlib的线程才能执行。使用`pj_thread_register()`即可。
但是在某些环境下，仍旧会crash，查看堆栈信息是`assert(mutex->owner()!=pj_thread_this())`这里。
查看源码，发现该段代码是包含在`PJ_DEBUG`的宏内，我们需要PJ_DEBUG的宏注释掉就好了，或者`#define PJ_DEBUG 0`.

具体编译方法可以参见`pjlib/include/pj/config_site_sample.h`里MAX_SPEED的配置。