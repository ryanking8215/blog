---
title: 资源，认证，鉴权和python的装饰器
date: 2015-04-12T16:50:54+08:00
categories: ["Tech"]
tags: ["python"]
slug: py-decorate
summary: 在一个web项目中使用python装饰器的经验
---

# 简述
这是一个目前在做的flask web项目的一点记录，基本思路是以python的装饰器为request handler加入资源描述，用户认证和鉴权的功能，这样，不用在每个request handler里都把这些代码调用一遍，以装饰器的模式，更加简便和美观，便于调试

下面描述几个概念
## 资源
这里的资源即人为设定的数据结构，用来描述该request handler会对系统的哪个资源进行什么样的操作。以restful api为例，你需要定义系统中有哪些
资源，该handler是做什么操作(CRUD)。以博客为例：
```python
class Resource(enum.IntEnum):
    BLOG = 1
    COMMENT = 2

class Operation(enum.IntEnum):
    C = 1<<0
    R = 1<<1
    U = 1<<2
    D = 1<<3
```
用户登录之后，得到资源数据，即BLOG资源可以有哪些操作，COMMENT资源有哪些操作，然后和handler的资源描述一比较，就能得到权限结果。

## 认证和鉴权
好多人认为这是一个东西，有些web框架也会认为是一个，但是依本人愚见不是，认证是用户以用户凭证是否能登录进你的系统，而鉴权是用户认证完后得到的权限能做什么操作。
2者有先后的逻辑关系。认证的方法有好多种，目前的系统是通过Digest来认证，简单方便。

详细说说鉴权，用户登录完后，从系统中取出该用户的权限操作，我这里以dict[Resource] = operation_mask来保存，即权限是一个dict，记录每个资源的操作值。当访问restful api时，
和handler的资源描述比对，其实就是检查dict内是否有对应的资源，通过位操作判断是否有对应的操作权限。简单方便。

## 装饰器
有追求的python码农都会考虑通过装饰器来简化函数调用。如果不使用装饰器，代码应该是这样的：
``` python
def get_blog():
   set_resource(BLOG,R)
   if not digest_authentication():
       abort(401)
   if not authorization():
       abort(403)
   # 继续处理
```

如果用装饰器，那么应该是这样的
``` python
@set_resource(BLOG,R)
@digest_authentication
@authorization
def get_blog():
   # 继续处理
   pass
```
有追求的python码农不会满足于此，每个函数上有3个@,其实本人的项目都是json输出，最后还有@jsonify的装饰器，总共有4个，太多太杂，而且有先后顺序，容易错。
整成一个多好？
``` python
@access_config((BLOG,R),is_authentication=True,is_authorization=True)
def get_blog():
    # 继续处理
    pass
```

有没有点`pyramid`的感觉？我们来定义一下access_config这个装饰器:

``` python
def access_config(resource_authority, is_authentication=True, is_authorization=True):

    ''' 访问设置, 用于简化处理函数的装饰器安装, 装饰器模式
        :param authority: 访问所需的权限值
        :param is_authentication: 是否认证
        :param is_authorization: 是否鉴权,如果is_authentication=False,则该值也无意义
    '''

    def _deco(func):
        @wraps(func)
        def _deco2(*args,**kwargs):
            f = func
            f = jsonify(f)
            if is_authorization:
                f = authorize(f)
            if is_authentication:
                f = authenticate(f)
            f = access_authority(resource_authority)(f)
            return f(*args,**kwargs)
        return _deco2
    return _deco
```
一个是要注意调用装饰器的顺序，另外，在`access_config`里设置参数，可以为每个handler单独设置是否需要认证和鉴权，便于调试，当然，默认值都是True，调用层参数更少。
大概就是这么个思路，记录一下，希望有帮助。

