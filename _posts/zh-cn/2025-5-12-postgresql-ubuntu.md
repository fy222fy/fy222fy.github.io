---
layout: post
title: ubuntu系统安装postgresql数据库
date: 2025-05-12
description: ubuntu安装postgresql并启动远程访问
tags: linux
categories: learn
---

## 安装

通过apt可以直接安装

```shell
sudo apt update
sudo apt install postgresql postgresql-contrib

```

## 配置

```shell
sudo -u postgres psql -c "SELECT version();"
# 切换用户到postgres以使用psql访问数据库
sudo su - postgres
psql
# 创建角色
createuser john
# 设置密码（需先创建用户）
psql -c "ALTER USER username WITH PASSWORD 'yourpassword';"
# 创建数据库
createdb johndb
```

## 配置远程访问

要修改两个文件

```shell
# 修改 /etc/postgresql/16/main/postgresql.conf
# 注意一定要用单引号
listen_addresses = '*'
```

```shell
# 修改 /etc/postgresql/16/main/pg_hba.conf
# 这一步主要是为了允许远程客户端访问
host  all all your.ip/24 md5
```

## 检查状态

重新启动并检查状态，注意由于postgresql服务不只一个服务，直接执行服务查询，状态显示可能为active(exited)。
请使用如下方式检查数据库是否运行正常：

```shell
# 重启
systemctl restart postgresql
# 检查运行状态
systemctl status 'postgresql*'
```

## 修改数据库地址

由于数据库存储内容很大，硬盘可能不够，需要修改保存地址。
首先通过如下命令检查当前保存目录：

```shell
psql
SHOW data_directory;
```

随后停止服务，进行数据迁移：

```shell
sudo systemctl stop postgresql
# 迁移原有内容
cp -Rp /var/lib/postgresql/16/main/* /your/newdata/dir/postgres
# 修改目录权限（仅postgres用户读写）
sudo chown -R postgres:postgres /your/newdata/dir/postgres
sudo chmod -R 700 /your/newdata/dir/postgres
```

修改数据库保存路径：

```shell
# 修改路径 /etc/postgresql/16/main/postgresql.conf
data_directory = '/your/newdata/dir/postgres'
```

重新启动数据库即可。
