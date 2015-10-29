Title: python ctypes
Category: tech
Date: 2015-09-20 14:50:54
Tags: python ctypes
Slug: python-ctypes
Summary: 使用ctypes封装libpcap时的一些心得
---

项目中需要用到python来抓网络包进行分析，看了pip有现成的pcap库，但是没用过，我使用的pcap的接口很简单，所以就想自己封装一个。

# 函数接口通过指针传递数据，如何在python中hold住内存
有接口
    pcap_next_ext(pcap_t *, pcap_pkthdr *, u_char **)

最后的参数即返回函数内部的内存指针，即该指针指向内部内存，该部分数据即收到的包，在处理协议时，需要对该数据包进行分析:
```c
    u_char * data;
    pcap_next_ext(pcap,&head,&data);
    eth_frame_t *eth = (eth_frame_t *)data;
    rest_data_t * mine = (rest_data_t *)(data+sizeof(*eth))
```
以上是c的调用实例，现在要用python来实现。

函数声明:
```python
    api.pcap_next_ext.argtypes = (ctypes.c_void_p,pcap_pkther_p, POINTER(POINTER(c_ubyte)))
```
这里用POINTER(POINTER(c_ubyte))来表示u_char **的类型，为什么不用
`POINTER(c_char_p)`呢，因为`c_char_p`是以NULL为结束的，所以分析二进制数据的时候，这个是不合适的，因为数据有可能为0,即’\0’,会被截断的。
调用：
```python
    data = POINTER(c_ubyte)() # u_char *data;
    api.pcap_next_ext(pcap,ctypes.byref(head),ctypes.byref(data))
```
这样，data就能hold住c function通过指针返回的数据了。
ctypes.byref(data)即 &data.

那如何使用data所指向的数据呢?
在python层，它认为是一个pointer, data有contents属性，值是第1个数据，即data[0],当然，我们可以通过data[i]访问索引为i的字节，和c指针一样，但如何强制转换呢？
eth_frame = ctypes.cast(data,eth_frame_p)
那之后的mine指针怎么赋值呢？
``` python
    mine = ctypes.cast(data+eth_frame.size(),rest_data_p)
```
这样是不行的，我们需要得到data的地址，通过ctypes.addressof(data.contents)
这才是data指针的基地址，我们可以通过它来访问后续的内存
``` python
mine = ctypes.cast(ctypes.addressof(data.contents)+eth_frame.size(),rest_data_p)
```

