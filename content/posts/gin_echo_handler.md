---
title: "Gin和Echo的handler在处理时的不同"
date: 2018-12-25T10:20:39+08:00
categories: ["Tech"]
tags: ["golang", "web", "webframework"]
keywords:
  - golang
  - gonic-gin
  - gin
  - Gin
  - echo
  - Echo
  - web框架
  - web framework
description: gin和echo框架的handler在处理时的不同
draft: false
---

# 引子
[Gin](https://gin-gonic.com/)和[Echo](https://echo.labstack.com/)都是我很喜欢的web框架。

它们2个对于Handler函数的定义略有不同.

* Gin
```golang
type HandlerFunc func(*Context)
```

* Echo
```golang
type HandlerFunc func(Context) error
```

HandlerFunc定义不同, Echo比Gin多返回了error。

写Restful业务时，一般正常情况下返回数据，错误情况下需要返回错误号，或者一个错误对象，该对象包含错误号和错误消息或其他信息. 我们看下在Gin框架下如何构建。

# Gin
先定义Error，Resonses数据结构，然后定义response函数.
```golang
type Error struct {
    HttpCode int         `json:"-"`
    Code     int         `json:"code"` // 这个是业务层的错误号，非Http Status Code
    Reason   interface{} `json:"reason"`
}

type Response struct {
    Error    *Error      
    Content  interface{}
}

func response(c *gin.Context, rsp *Response) {
    if rsp.Error!=nil {
        c.JSON(rsp.Error.HttpCode, rsp.Error)
        return
    }
    c.JSON(rsp.Content)
}
```

Handler使用:
```golang
func GetXXX(c *gin.Context) {
    rsp := &Response{}

    defer response(rsp)

    xxx, err := xxxSvc.Get()
    if err!=nil {
        rsp.Error = &Error{HttpCode: http.StatusInternalServerError, Code:1000, Reason:err}
        return
    }
    rsp.Content = xxx
    return
}
```

这里要注意的是`defer`, 千万不能写成:
```golang
var rsp Response
defer response(&rsp)
```
`defer`在处理时，会先对函数参数求值，如此一来，rsp里都是0值，无论之后rsp再如何赋值，最终response处理的都是0值。

可以像上述那样使用指针，也可以使用匿名函数来wrap一下:
```golang
var rsp Response
defer func() {
    response(&rsp)
}()
```

# Echo
Echo的HandlerFunc返回error，当然我们可以不理会这个error, 那么和Gin的处理方式一样了。

当然也可以利用这个error，如果我们返回error，Echo能够按照我们的协议输出error信息，正常的信息归正常的信息返回，岂不美哉.

先定义错误对象
```golang
type Error struct {
    HttpCode int         `json:"-"`
    Code     int         `json:"code"` // 这个是业务层的错误号，非Http Status Code
    Reason   interface{} `json:"reason"`
}
```

首先要做的，是看下Echo能否支持自定义的错误处理，只有支持了，我们才能截获错误，并按照我们的要求输出。

```golang
// 自定义错误处理函数
func ErrorHandle(err error, c echo.Context) {
	switch e := err.(type) {
	case *Error:
		code := e.HTTPCode
		c.JSON(code, e)
	default:
		c.Echo().DefaultHTTPErrorHandler(err, c)
	}
}

// 替换默认的错误处理
e := echo.New()
e.HTTPErrorHandler = ErrorHandle
```

有了错误对象和自定义的错误处理，来看下在Handler里如何使用

```golang
func GetXXX(c echo.Context) error {
    xxx, err:= xxxSvc.Get()
    if err!=nil {
        return &Error{HttpCode: http.StatusInternalServerError, Code:1000, Reason:err}
    }
    return c.JSON(http.StatusOK, xxx)
}
```

利用了error以后，HandlerFunc的代码会简洁很多，而且符合go-style的错误处理方式.