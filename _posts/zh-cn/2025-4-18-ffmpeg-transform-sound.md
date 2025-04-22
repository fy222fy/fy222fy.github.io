---
layout: post
title: 使用ffmpeg将声音从不同设备转移
date: 2025-04-09 23:17:00
description: ffmpeg
tags: linux
categories: learn
---

## 背景

希望通过网络让设备A作为音频输入，设备B作为音频输出。

以mac作为麦克风，windows作为音响为例。

## 安装ffmpeg

对于mac系统：

```shell
brew install ffmpeg
```

对于windows系统，访问官网，下载发布版本压缩包，解压，并将 bin文件放到环境变量即可。
注意，这里由于还要以来其他dll文件，所以直接执行ffmpeg二进制程序不可取。

## 配置mac端

配置mac作为发送端：

```shell
ffmpeg -f avfoundation -i ":0" -c:a libmp3lame -f rtp rtp://<接收端ip>:<端口>
```

## 配置windows端

```shell
ffmplay -i rtp://<发送端ip>:端口
```
