---
layout: post
title: 插入新pci设备后ubuntu网络不可用
date: 2025-04-09 23:17:00
description: 双系统安装
tags: linux
categories: learn
---

## 背景

自己搭建的服务器，ubuntu本来网络是好的，结果购买了一块新的m2硬盘，插入后发现网络模块不能用了。

并且发现，插入新的显卡（任何pci）设备，都会导致网络不能用。
本来以为是pci线路冲突导致的，后来发现根本也㽸是插入设备后，命名改变导致的。

## 确认命名问题

通过`ip a`查看网卡名称，我这里的网卡名称是`enp4s0`。

导航到`/etc/netplan/`，查看netplan配置：

```shell
vim /etc/netplan/50-cloud-init.yaml
```

其中配置项中，可以看到当前默认配置的网卡，我这里是`enp3s0`，可以判断是之前的网卡命名，由于插入了新的设备，导致名称发生变化。

## 解决

解决方式很简单，将netplan配置文件中的网卡名称统一替换成`enpp4s0`，随后apply即可：

```shell
netplan apply
```
