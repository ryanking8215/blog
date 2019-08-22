---
title: promise处理数组
date: 2014-10-05T16:47:03+08:00
categories: ["Tech"]
tags: ["javascript"]
slug: promise-process-array
summary: 使用promise处理数组的方法和要注意的问题
---

promise 使用bluebird，现在要求按照数组顺序启动异步任务，也即等待一个promise被settled后再执行下一个。
有什么方法吗？难道按照数组写死一个个的then吗？
<!-- more -->

### Promise.map()
Promise.map() 是按顺序迭代数组，但是异步任务仍旧是并发执行的。不符合条件。

### 递归
``` javascript
var array = ['a1','a2','a3','a4']

return (function handle_array(idx){
    idx = idx || 0
    if (idx>=array.length) {
        return
    }
    return async_task(id,array[idx])
    .then(function(result){
        idx++;
        return handle_array(idx);
    })
})()
```

### 利用promise对象迭代
``` javascript
var promise = Promise.resolve()
array.forEach(function(v){
    console.log(v)
    promise = promise.then(function(){
        return async_task(v)
    })
    .then(function(v){
        console.log(v)
    })
})
promise.then(function(){
    console.log('done')
})
```

可能还有其他方法。
个人感觉递归更自然一点。
第二种方法要记住promise可以先返回，但是按照顺序被resolved后再执行下一个的。
