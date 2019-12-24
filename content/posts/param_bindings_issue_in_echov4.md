---
title: "Echo.v4的参数绑定问题"
date: 2019-11-13T14:54:28+08:00
categories: ["Tech"]
tags: ["golang"]
slug: param_binding_issue_of_echov4
keywords:
  - Echo
  - Echo.v4
  - 参数绑定
  - Restful API
decription: Echo.v4 有一个参数绑定问题，造成restful api开发的困扰。

draft: false
---

# 现象
[Echo](https://echo.labstack.com/)是golang语言开发的，高性能, 可扩展的微型web框架。

笔者在项目中一直使用Echo框架，一直是v3.x的版本，在项目达到一定阶段后，发现Echo已经发布了"v4"版本一段时间，于是想把框架升级成v4.
到目前为止，最新的版本是`v4.11`

升级之后，发现有些请求出现了问题，具体报错为:
```shell
"binding element must be a struct" introduced with path params binding
```

升级后编译一把过，说明API设计的兼容性没有问题，现在是运行时报错了。

整个demo来验证这个问题, 这个demo是典型的restful应用，url里的参数表示资源id，body传入数据:
``` golang
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
    "github.com/labstack/gommon/log"
)

func main() {
    s := echo.New()
    s.Use(middleware.Logger())

    s.PUT("/users/:id", func(c echo.Context) error {
        var data interface{}
        if err := c.Bind(&data); err != nil {
            log.Fatal(err)
        }
        log.Print(data)
        return nil
    })

    s.Start(":8811")
}
```

请求:
```shell
curl -X PUT -H "Content-Type: application/json" -d '{"name":"John"}' localhost:8811/users/1
```

例子很简单，有一个URL请求是`POST /users/1`, 传入的body是json `{"name":"John"}`.

这个例子造成Echo在调用c.Bind时报错。

我们看下Echo `Bind`的源码:
```golang
// Bind implements the `Binder#Bind` function.
func (b *DefaultBinder) Bind(i interface{}, c Context) (err error) {
        req := c.Request()

        names := c.ParamNames()
        values := c.ParamValues()
        params := map[string][]string{}
        for i, name := range names {
                params[name] = []string{values[i]}
        }
        if err := b.bindData(i, params, "param"); err != nil {
                return NewHTTPError(http.StatusBadRequest, err.Error()).SetInternal(err)
        }
        if err = b.bindData(i, c.QueryParams(), "query"); err != nil {
                return NewHTTPError(http.StatusBadRequest, err.Error()).SetInternal(err)
        }
        if req.ContentLength == 0 {
                return
        }
        ctype := req.Header.Get(HeaderContentType)
        switch {
        case strings.HasPrefix(ctype, MIMEApplicationJSON):
                if err = json.NewDecoder(req.Body).Decode(i); err != nil {
                        if ute, ok := err.(*json.UnmarshalTypeError); ok {
                                return NewHTTPError(http.StatusBadRequest, fmt.Sprintf("Unmarshal type error: expected=%v, got=%v, field=%v, offset=%v", ute.Type, ute.Value, ute.Field, ute.Offset)).SetInternal(err)
                        } else if se, ok := err.(*json.SyntaxError); ok {
                                return NewHTTPError(http.StatusBadRequest, fmt.Sprintf("Syntax error: offset=%v, error=%v", se.Offset, se.Error())).SetInternal(err)
                        }
                        return NewHTTPError(http.StatusBadRequest, err.Error()).SetInternal(err)
                }    
         ....                     
```

可以看到，它先`bindData params`, 而这个`param`，即传入的"id". 即Echo先尝试绑定param，在"ContentLength>0"时再绑定body。

和我们预想的使用`c.Bind()`来获取`body`数据不符。而查看"v3"版本的，是没有这个问题的。

# 解决方法
可以通过不同方法绕过c.Bind调用。

1. 使用json.NewDecoder()或者json.Unmarshal()替换c.Bind
2. echo支持自定义Binder对象，`echo.Binder = MyBinder()`

# 后记
笔者把该问题反馈给了上游, 发现有人已经提过[issue](https://github.com/labstack/echo/issues/1356), 我再补充一下。

作者之一貌似准备重新release一个版本。

我提出来是否可以用一个选项来开关该功能(param binding).