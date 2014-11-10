title:  使用n来管理nodejs的version
date: 2014-11-10 21:53:33
categories: tech
tags : [nodejs]
---

想尝试一下ec6的generator和co,为了不影响原有的开发环境
使用n来管理nodejs的版本。

n的使用还是很简单的：
```shell
n latest
n stable
```
分别安装最新发布版本和稳定版本，前者带有ec6支持，后者用于开发环境。
这2个都是安装的二进制版本，不需要编译。

单独使用`n`可以切换版本号，但我的目的是二者共存，`n`还有个命令：
```shell
n use <version>
```
只要把这个写个alias到shell里，就能共存啦：
```shell
alias nn="n use 0.11.14 --harmony"
```
想尝试generator的，只要`nn xxx.js`就好啦！很方便。

p.s. 之前还用了一小会nvm，是从源码编译node的，在Linux上切换发生了点问题，具体
原因也不查了，it makes no sense. 感觉没`n`好用。