---
layout: post
title: 配置新的linux服务器并安装iterm2
date: 2024-12-30 16:40:16
description: 服务器部署
tags: linux
categories: learn
---

## 配置iterm2自动登录服务器

1. 打开settings-Profiles；
2. 新增一个Profile；
3. 在Command-General，选择Command，键入：ssh xxx@xx.xx.xxx.xx；
4. 选择Command-Advanced-Triggers-Edit；
5. 在Regular Expression中，键入xxx@xx.xx.xxx.xx's password，目的是捕获服务器端的返回；
6. Action选择Send Text
7. Parameters中键入服务器密码，注意后面加上`\n`，不然不会自动登录；
8. 后面的Instant、Enable都开启。

## Linux服务器配置新用户

1. 增加用户：useradd xxx -m
2. 修改密码：passwd xxx
3. 配置sudo用户组: usermod -G root xxx
4. 允许用户ssh登录：

## Linux Ubuntu安装oh my zsh

1. 安装zsh：sudo apt install zsh -y
2. 切换zsh为默认shell：chsh -s /bin/zsh
3. 安装oh my zsh：sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
4. 编辑配置: vim ~/.zshrc
5. 切换主题：ZSH_THEME="agnoster" # last: "robbyrussell"
6. 语法高亮：git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~
   /.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
7. 自动补全：git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~
   /.oh-my-zsh/custom}/plugins/zsh-autosuggestions
8. 记得在配置中增加：

```text
plugins=(
        git
        zsh-syntax-highlighting
        zsh-autosuggestions
)
```
