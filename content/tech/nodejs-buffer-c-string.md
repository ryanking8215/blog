Title:  nodejs的buffer和c string
Date: 2014-10-31 19:13:42
Category: Tech
Tags: nodejs
Slug: nodejs-buffer-cstring
Author: Ryan King
Summary: nodejs的buffer和c string如何转换,二进制协议用得到

设备上有现成的二进制通信协议，nodejs作为客户端连接上去发送请求得到响应。
其中有协议是传送字符串，用`c struct`表示就是
```c
struct Response {
    uint32_t value;
    char name[64];
};
```
因为c string以'\0'为结束，为了协议到c的对端能开箱即用，name最多存63个字节。

node客户端收到数据后，用buffer来处理，转换成response对象
```javascript
{
    value: {number}
    name: {string}
}
```
buf转string的函数是 `buf.toString()`，但是得到的数据类似于
```javascript
'h','e','l','l','o','\u0000','\u0000'
```
因为js的string不是以'\0'结束，它把后面的都处理为字符串的一部分，所以我们要处理一下：
```javascript
name = name.substring(0,name.indexOf('\u0000'))
```
这样就ok了

### 编码问题
默认的hex和utf8,nodejs的buffer api都能处理，但是如果是其他编码呢？比如由于历史原因，设备上
传输的中文编码是gb2312。
很幸运的是，npm里有iconv-lite的package，它能将不同的编码从string->buffer, buffer->string的转换。
用它就能开心的撸了！
