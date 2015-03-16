Title: git远程的仓库和分支操作
Date: 2014-10-05 17:00:20
Category: tech
Tags: git
Slug: git-remote-summary
Summary: 简单操作，简单记录

看了git的手册，关于remote的操作。稍微精简了一下，以供记录和记忆。

1. 查看远程仓库
		git remote [-v]

2. 添加远程仓库
		git remote add [remote-name] [url]

3. 改名远程仓库
		git remote rename [old-name] [new-name]

4. 删除远程仓库
 		git remote rm [remote-name]

5. 抓取远程仓库的数据
		git fetch [remote-name]
   
6. 推送数据到远程分支
		git push [remote-name] [branch-name]
		git push [remote-name] [local-branch-name]:[remote-branch-name]

7. 删除远程仓库分支
		git push [remote-name] :[remote-branch-name]

8. 使用本地分支跟踪远程分支
		git checkout --track [remote-name]/[remote-branch-name]
		git checout -b [local-branch-name] [remote-name]/[remote-branch-name]

9. 如果本地分支为跟踪分支：
  在此分支下 git pull（fetch and merge）, git push可以自动识别远程信息，不需要填写remote-name/branch-name了。包括git clone来分支的。

10. 合并本地分支和远程分支
		git merge [remote-name]/[remote-branch-name]
