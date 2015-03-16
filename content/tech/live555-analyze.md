title:  Live555源码分析
date: 2014-10-04 22:13:35
category: tech 
tags: live555
Slug: live555-analyze
Summary: 不定时更新...

## Source
Live555下FramedSource是继承于MediaSource的类，表示**提供帧数据源**,
主要用“模板模式"实现了getNextFrame()接口，其中doGetNextFrame()需要子类去实现。

## Source级联
大部分的Source类都继承自FramedFilter类而不是FramedSource，
FramedFilter本身是一个FramedSource类，而且可以有一个FramedSource类对象作为input，
这样FramedFilter就可以级联起来，对用户使用来说，
live555不主动定义现有的FramedSource，因为每个用户的数据来源广泛，
用户只要实现了自己的FrameSouce类，然后就可以使用现有的FramedFilter类做处理。

例如，我只要实现自己的FrameSource类，或从网络自有协议获取数据，
或从设备直接编码得到数据，
然后通过live555的现有H264VideoStreamFramer->H264FUAxxx->H264RTPSink,这样利用live555，实现h264的rtp封装。

## 补充
如果直接从RTP流获取数据作为Source,live555有现成的RtpSource和N种媒体类型对应的RtpSource子类。

如果从设备直接编码数据，可以继承DeviceSource类，这是live555预先定义好的抽象类.
