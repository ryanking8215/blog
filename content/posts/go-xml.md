---
title:  golang and xml
date: 2014-10-04T22:13:33+08:00
categories: ["Tech"]
tags: ["golang", "xml"]
slug: golang-and-xml
keywords:
  - golang
  - xml
description: golang使用xml的方法，比如有些协议里根据command不同，content也不同，如何处理呢？
---

golang使用encoding/xml的**Marshal**和**Unmarshal**来处理xml。这个很简单，而且官网上都有例子。
官网上的例子都是解析某个文件，文件的内容都是确定的；或者通过某个确定的struct来生成xml，struct的定义也是确定的。

但是在处理网络协议的时候，协议是变化的，例如协议有协议头，有msg_type表示是request还是response,每个request和response
根据不同的command，带有不同的content：比如command="do_a"或"do_b",带的content不一样，就算一样的command，request的content和
response的content也不一样，那收到协议以后如何解析呢？连内容都确定不了，没有办法定义一个确定的struct去Unmarshal

<!--more-->

## 一开始的方法
一开始想到的方法是用一个struct，把协议头，msg_type,command，request和response都包含在内，Unmarshal后
按照msg_type和command,让调用者自行取content.这个都解析是每问题的，但是marshal时出现问题了，我填了request，但是
response也marshal出来了。

## omitempty
查看文档，xml有一个omitempty的属性，针对golang的各类型的变量如果为初始值，则认为是empty,不marshal.但是在上述例子上，由于request
and response都是内嵌在Message内的变量，所有就算content被omit了，但是rsp/req的标签还是存在的。so这个路子也走不通。

## pointer and omitempty
晚上看纸牌屋时，还在思考这个问题，突然灵光一闪，既然用omitempty，那指针如果为nil肯定被omit，那么把request和response变成指针就ok了。
好的，marshal没问题了。但是unmarshal呢？由于是指针，是不是需要事先为它分配内存呢？做了一个实验，不分配内存，也没报错，难道是xml的package内部
会new一个吗？没有去读源码考证，以后空下来去研究一下，这边存怀疑态度。


