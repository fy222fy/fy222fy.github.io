---
layout: post
title: 服务器安装linux和ubuntu双系统
date: 2025-04-09 23:17:00
description: 双系统安装
tags: linux
categories: learn
---

## 背景

在一台服务器上，有可能需要同时安装linux和windows双系统，
这时存在如何设置grub启动双系统的问题。

在我个人的情况中，是首先在磁盘A安装了ubuntu系统，随后在磁盘B安装Windows系统，但发现最后只能登入ubuntu系统，无法登入Windows。

## 设置引导程序

首先在ubuntu中，尝试直接执行：

```shell
sudo update-grub
```

如果没问题的话，可以直接检测到windows系统。

但可能出现错误：`Warning: os-prober will not be executed to detect other bootable partitions. Systems on them will not be added to the GRUB boot configuration.`

第一种可能是没有安装`os-prober`，使用如下命令安装：

```shell
sudo apt-get install os-prober
```

再次执行，如果还出现相同问题的话，查看`/etc/default/grub文件`，
确保没有禁用os-prober的行，新版默认应该是禁用的，所以这里应该改成false：

```shell
GRUB_DISABLE_OS_PROBER=false
```

再次执行，应该就找到了。

如果还是不行，应当配置文件`/etc/grub.d/40_customs`：

```text
menuentry "Microsoft Windows 11" {
insmod part_gpt
insmod chain
insmod ntfs
search --fs-uuid --no-floppy --set=root 【序列号】
chainloader (${root})/efi/Microsoft/Boot/bootmgfw.efi
}
```

其中，【序列号】替换为你Windows系统安装分区的序列号，可以用如下命令查询：

```shell
sudo blkid
```
