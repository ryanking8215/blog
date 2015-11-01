Title: 不要strip ko文件
Date: 2014-06-04 22:20
Category: Tech
Tags: linux, c
Slug: dont-strip-ko
Author: Ryan King
Summary: 闹乌龙啦...

今天给嵌入式linux系统做升级包，发现升级包有点大，于是把lib下和bin下的
文件都strip了一下，手痒了，把lib/modules/下的ko也strip了一下。

还好测试了一下升级包，设备重启后无法加载内核模块，这才发觉，我把ko的symbols都
strip了，内核当然无法加载ko了。

切记，切记！
