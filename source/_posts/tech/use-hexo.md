title: 使用hexo
date: 2014-10-04 15:46:33
tags:
---

## 第一次
第一次使用hexo，一开始没有填deploy,然后直接`hexo deploy`在本地部署。
之后再填了deploy信息，但是在`hexo deploy`时报
``` bash
On branch gh-pages
nothing to commit, working directory clean
error: src refspec master does not match any.
error: failed to push some refs to 'https://github.com/ryanking8215/ryanking8215.github.io.git'
```

把`ryanking8215.github.io.git`仓库删除再重建还是不对。后来网上找到方法`rm -rf ./deploy`,重新部署就OK了。

## 改进
发现生成的网页的用了google的cdn，对墙不友好，需要修改。
另外需要增加评论系统，最好是本土化的，例如多说等。
可能还需要再重新配置一下theme，hexo默认的landscape还是不错的。