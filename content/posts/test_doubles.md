---
title: "测试替身，Fake,Stub,Mock"
date: 2019-12-31T11:42:52+08:00
categories: ["Tech"]
tags: ["testing", "测试"]
keywords:
  - testing
  - 测试
  - mock
description: 描述了3种测试替身类型, 并且使用go实现example
draft: true
---

最近在网上看到[这篇博文](https://dev.to/milipski/test-doubles---fakes-mocks-and-stubs), 博文介绍了几种"测试替身"的方式和Java例子。

这里进行简单的翻译，并给出golang的example.

>In automated testing it is common to use objects that look and behave like their production equivalents, but are actually simplified. This reduces complexity, allows to verify code independently from the rest of the system and sometimes it is even necessary to execute self validating tests at all. A Test Double is a generic term used for these objects.


在自动化测试领域，普遍使用更简化的对象来测试。这减少了复杂度，并且能和系统其它部分做很好的隔离，可以单独验证。这种对象有个术语，叫"测试替身"。


>Although test doubles come in many flavors (Gerard Meszaros introduced five types in this article), people tend to use term Mock to refer to different kinds of test doubles. Misunderstanding and mixing test doubles implementation may influence test design and increase fragility of tests, standing on our way to seamless refactorings.

"测试替身"有好几种方式([这篇文章](http://xunitpatterns.com/Test%20Double.html)介绍了有5种), 人们一般都是用术语"Mock"来指代这些不同类型的"测试替身"。误解和混淆这些测试替身会影响测试设计，增加测试脆弱性，阻碍我们的持续重构。

>In this article I will describe three implementation variations of testing doubles: Fake, Stub and Mock and give you examples when to use them.

作者介绍3种"测试替身"的实现，Fake, Stub和Mock, 并且给出例子说明什么时候去使用。

## Fake
> Fakes are objects that have working implementations, but not same as production one. Usually they take some shortcut and have simplified version of production code.

Fake对象有可工作的实现，但是和生产环境的不同。通常他们是生产环境代码的简化版本.

![](/images/test_doubles/fake.png)

## Stub
>Stub is an object that holds predefined data and uses it to answer calls during tests. It is used when we cannot or don’t want to involve objects that would answer with real data or have undesirable side effects.

Stub对象在测试过程中使用预定义的数据响应外部调用。当我们不能或不想引入真实数据的响应，或者不想有副作用时使用。

![](/images/test_doubles/stub.png)

## Mock
>Mocks are objects that register calls they receive. In test assertion we can verify on Mocks that all expected actions were performed.

Mock对象记录他们接收到的调用，在测试过程中我们通过检查Mock对象来确认所有的预期动作被执行了。

![](/images/test_doubles/mock.png)

# 后记
### Stub和Mock的区别

# 参考
* https://dev.to/milipski/test-doubles---fakes-mocks-and-stubs
* https://zhuanlan.zhihu.com/p/26942686

