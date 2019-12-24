---
title: promise要注意的地方
date: 2014-10-05T16:50:54+08:00
categories: ["Tech"]
tags: ["javascript"]
slug: promise-stuff
keywords:
  - javascript
  - promise
description: 使用promise是一些注意的问题，不定时更新...
---

promise可以级联，但是不要忘记在then()中return一个Promise,否则将会并发执行。

``` javascript
do_a()
.then(function(){
      do_b()
})
.then(function(){
     do_c()
})
```

VS.

``` javascript
do_a()
.then(function(){
      return do_b()
})
.then(function(){
})
```

**切记！**