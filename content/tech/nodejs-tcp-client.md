Title:  如何使用nodejs撸一个tcp client
Date: 2014-10-28 22:20
Category: tech
Tags: nodejs
Slug: nodejs-tcp-client
Author: Ryan King
Summary: 用nodejs实现一个可实用的tcp client,不只是回调那么简单。

单看话题有点low,用nodejs撸一个tcp client不是秒秒钟的事情
封装一个client，sock收到data后解析出msg，通过event通知调用端msg来了：
```javascript
var sock = net.createConnection(...);
sock.on('error',function(){
	
})
sock.on('data',function(buf){
	var msg = parse_data(buf)
	self.emit('msg',msg)
})
```
大意如此，不要在意细节。如果真是这样的话，那就没有必要撸这个博文了。

首先要看封装的api到什么程度，client.sendRequest()之后如果什么都不干，光等msg过来，对于
调用你client库的主来说真的是苦主了，一般client都有业务逻辑在，例如先connect(),再login(),
然后再干嘛干嘛；也需要判断response，你都放在`client.on('msg',function(){...})`里，让别人情何以堪。

那应该怎么做呢？

<!--more-->

### API设计
我们让client api好用一点，一般是这样子的：
```javascript
client.sendRequest(msg,function(err,result){})
```
或者这样子的:
```javascript
client.sendRequest(msg) -> Promise(result)
```
前者通过回调函数返回错误或结果，后者通过Promise返回，本质是一样的。
因为server消息需要异步处理，所以我们需要callback或者promise来返回结果。

### 实现
api的方式确定下来了，那么要研究如何实现了，假设用callback方式吧，这也是目前nodejs的api的标准格式。
server的数据是通过socket的`data`事件来的，client.sendRequest(msg,cb)函数里，会有cb这个参数，如何把它们联系起来呢？
只要收到消息之后执行cb()，就可以通知调用端了。回复消息的处理在另一个函数上下文里，如果能把cb搬过去，在那个函数上下文执行就好了。
可以利用队列，当sendRequest()时，构建一个内部使用的request对象，将cb和请求参数塞入队列，
在`data`的事件处理中，从队列依次取出request对象，比对请求参数和回复消息，然后可以执行cb()函数了，这样调用端就会得到结果了。

用promise也是一样的，用defer代替cb，ok的就defer.resolve(result); 出现错误了就defer.reject(err)。
了解promise的都知道我在说什么，^_^

### buffer处理
tcp是流式的，没有消息边界，换言之，`data`事件回调里的buffer，不一定含有一条或者多条完整的协议消息，有可能是不完整的，有可能是多条完整加一点不完整的，
总之不能做假设任何，这是tcp的粘包问题，这也是为什么tcp协议都会设定同步头，数据长度或者数据分隔符的原因。
在收到data之后，需要和client的缓存拼接起来，看是否能parse出消息，如果能的，则需要把处理过的buffer都去除，
未处理的buffer留下来的，以待后用。
那如何维护这个缓存呢？看一下的demo
```javascript

Session.prototype.append = function(buf) {
    if (!buf)
        return

    if (!this._buf) {
        this._buf = buf
        this._buf_len = buf.length
        return
    }

    var left = this._buf.length - this._buf_len
    if (left>=buf.length) {
        buf.copy(this._buf,this._buf_len)
        this._buf_len+=buf.length
        return
    }
    this._buf = Buffer.concat([this._buf.slice(0,this._buf_len),buf])
    this._buf_len+=buf.length
}
```
就是维护一个_buf和_buf_len，前者表示缓存，后者表示数据大小，不是缓存容量大小。遵循以下规则:
- 如果没有，则新建。
- 如果buffer剩余空间比当前buffer大，则把当前buffer的数据copy进缓存
- 如果buffer剩余空间比当前buffer小，则将来缓存数据和buffer数据合并，作为新的缓存。

消息处理只要用到内部缓存就可以了。
这样在一定程度上避免了频繁申请内存。
但是频繁申请内存还是逃避不了，因为libuv在底层会一直接受数据，否则你以为回调函数里的buffer是哪里来的
这个和reactor模式不同，nodejs可以通过sock.pause(),sock.resume()控制接收速度，让内存不要增加太快。

另外由于v8对gc不那么积极，而且buffer的内存在v8的heap外，这样buffer会释放的更慢。
开源项目[shadowsock-nodejs](https://github.com/clowwindy/shadowsocks-nodejs)，作者之前因为内存暴涨问题，放弃了该版本。
不清楚nodejs对内存暴涨如何解决。本来nodejs最擅长的就是干这个事情，结果因为这个原因，反而不合适，是比较遗憾的。

欢迎大家探讨！




