title: promise要注意的地方
categories: tech
date: 2014-10-05 16:50:54
tags: [javascript]
---

promise可以级联，但是不要忘记在then()中return一个Promise,否则将会并发执行。
<!-- more -->

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