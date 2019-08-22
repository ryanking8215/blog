#!/bin/sh

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"
msg="rebuilding site `date`"
if [ $# -eq 1 ]; then
    msg="$1"
fi

# use -D to build draft too.
# use -t to choose theme
hugo

cd ./public
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/ryanking8215/ryanking8215.github.io.git
fi

git add -A
git commit -m "$msg"
git push -f origin master