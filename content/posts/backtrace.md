---
title:  "使用backtrace跟踪栈信息"
date: 2012-05-04T22:20:43+08:00
categories: ["Tech"]
tags: ["linux", "debug"]
keywords:
  - linux
  - 调试
  - stack
description: 使用backtrace跟踪堆栈信息
---

一种在嵌入式上可行的调试方法，截获SIGSEGV信号，并作backtrace()处理，把
调用栈信息打印出来。

``` c
#include <signal.h>
#include <execinfo.h>

int main(void)
{
    signal(SIGSEGV,DebugBacktrace);
}

static void  DebugBacktrace(int signal)
{
#define SIZE 100
    void *array[SIZE];
    int size,i;
    char **strings;
    char buf[50];

    fprintf(stderr,"\nSegmentation fault \n");
    size = backtrace(array,SIZE);
    fprintf(stderr,"Backtrace (%d deep):\n",size);                                                                              
    strings = backtrace_symbols(array,size);
    for(i = 0;i<size;i++)
    {
        fprintf(stderr,"%d: %s \n",i,strings[i]);
    }
    free(strings);
    exit(-1);
    return ;
}
#=> 会将调用栈根据需要显示出来
```

比起core来，不需要占用很大的空间，但是貌似只能回溯调用栈，无法回溯当时的内存。
