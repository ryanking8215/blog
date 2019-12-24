---
title: pyramid and flask
date: 2015-04-06T16:13:40+08:00
categories: ["Tech"]
tags: ["webframework","python"]
slug: pyramid-and-flask
keywords:
  - python
  - web开发
  - flask
  - pyramid
  - flask vs. pyramid
  - web框架
description: 两个python的web微框架的比较，还没到"vs."的境界，只好用"and"了, -)
---

有个企业内部项目，restful api，mysql, digest authentication.
python很早就用了，写一些维护的脚本和验证一些算法，简单明了，不用考虑c/c++的内存管理。
但是web开发还是第一次，事先了解了一些python下的web framework

- web.py
- bottle
- flask
- pyramid
- django

因为ORM使用sqlalchemy，所以先踢掉了django；web.py因为python3和创始人的原因，不再考虑；bottle太过简单，学习可以，用在工程上可能欠妥，也排除；留下了flask和pyramid，flask名气更响，资源更多，但是在简单了解了pyramid后，使用pyramid来开展项目，当然之后由于某些原因又换到了flask，所以把这2个框架的使用和区别做一些记录，以供参考，当然，由于初次接触web框架，难免会有疏漏和错误，望海涵。

## 路由
pyramid把url设置为一个唯一string,然后将hanlder绑定在该string上。几乎所有的配置均可通过装饰器解决，除了url本身，你可以指定method,query strings来绑定具体的handler，不用进一个进口，然后根据query stirng或者method来区分。

flask使用装饰器直接将url绑定在handler上，无论是使用app还是blueprint。支持继承view的方式来设定handler，我用的最多的就是MethodView。

## 模板
pyramid默认模板是mako；flask默认模板是jinjia2。按照jinjia2的说法，两者性能差不多，好像周遭用jinjia2的更多一点。两者均支持更换第三方模板。

pyramid支持将模板render功能写在装饰器里，而flask需要显式调用`render_template()`,我的项目返回json数据，pyramid支持内置的`render='json'`,而flask需要显式调用`jsonify`,后来项目换成flask的时候，也如法炮制，将render做成了装饰器。

## 测试
两者的测试哲学不同。

pyramid因为处理函数返回的数据是dict，所以，它的测试是直接对处理函数测试，将req填好数据，然后直接调用处理函数，得到dict，再验证dict正确性。

flask需要一个请求上下文来测试，也可以说是模拟一个请求客户端，填入真正的url和数据，返回的也是真的数据，而不是中间数据。

各有利弊，pyramid的这种方式测不到路由是否正确，flask如果用模板render,得到html，验证数据比较麻烦。

## python3支持
按照各自官网的说法，pyramid对python3完全支持。

flask本身支持，但是它认为好多add-on仍旧是python2,所以还是推荐python2.

## 更多
pyramid对web还有更多的框架定义，例如`security`,支持认证和权限等等。

flask更内聚一点，额外功能用addon实现。

## 总结
两者都是优秀的框架，项目换成flask不是因为flask比pyramid好，只是flask中文资源更多一点，因为初入web,找help更简单一点。
其实，pyramid的config装饰器功能强大，几乎配置均可以写在装饰器里，包括method，query string，render资源，不仅仅是url本身，我喜欢这种方式，似乎其他的web框架都没有这么强大的配置装饰器。
作为初入者，我不太明白为什么flask比pyramid更流行，从最后展现的框架上看，我认为pyramid更好，更符合工程需求，更完善。