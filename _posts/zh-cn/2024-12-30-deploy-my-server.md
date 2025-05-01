---
layout: post
title: 配置新的linux服务器并安装iterm2
date: 2024-12-30 16:40:16
description: 服务器部署
tags: linux
categories: learn
---

## 设置root密码

新安装的系统可能没有root账号密码，通过如下命令设置root账号密码：

```shell
sudo passwd root
```

## 配置本地iterm2自动登录服务器

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

## ubuntu设置静态ip

如果是服务器大多时候远程登录，有静态ip需求，则可关闭dhcp，设置静态ip。
配置静态ip的目录是`/etc/netplan/xxxx.yaml`。
注意修改前先备份。
配置静态ip的文件如下所示，注意是新语法，可能不适合老版本的ubuntu系统。

```yaml
network:
  version: 2
  ethernets:
    eno1:
      dhcp4: false
      addresses: [192.168.1.7/24] # 配置的地址
      optional: true
      routes:
        - to: default
          via: 192.168.1.1 # 路由地址
      nameservers:
        addresses: [192.168.1.1] # nameserver地址
```

配置完成后，使用如下命令验证并保存

```shell
sudo netplan apply
```

## 安装docker

- 更新系统包：首先，确保系统包是最新的：

```shell
sudo apt update
sudo apt upgrade -y
```

- 安装依赖包：安装 Docker 所需的依赖包：

```shell
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

```

-添加 Docker 官方 GPG 密钥：添加 Docker 的官方 GPG 密钥以确保下载的软件包是安全的：

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

```

- 添加 Docker 仓库：将 Docker 的稳定版仓库添加到 APT 源列表中：

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

- 更新包索引：更新 APT 包索引以包含 Docker 仓库：

sudo apt update

- 安装 Docker：安装 Docker CE（社区版）、Docker CLI 和 Containerd：

sudo apt install -y docker-ce docker-ce-cli containerd.io

- 启动并启用 Docker 服务：启动 Docker 服务并设置为开机自启：

sudo systemctl start docker
sudo systemctl enable docker

- 验证安装

```shell
docker ps
```

- 用户组设置，给sudo以外用户使用

```shell
sudo groupadd docker
sudo usermod -aG docker username
```

注意执行完命令后要重新登录用户生效。

## 安装docker-compose

```shell
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

## 设置代理

首先下载代理请按照各代理要求下载，注意下载对应配置文件。

不想通过dashboard来配置代理，可以创建如下脚本`select_proxy.sh`，用于通过命令行交互来动态选择代理，记住脚本创建的位置。

```shell
# 选择代理节点
select_proxy() {
    local secret=$1
    if [ -z secret ]; then
      secret="Proxy"
    fi
    # 使用您的命令获取代理节点列表
    # ============= 修改此处 =============
    proxies=$(curl -s -XGET -H "Content-Type: application/json" -H "Authorization: Bearer ${secret}" 127.0.0.1:9090/proxies | jq -c '.proxies.GLOBAL.all')
    echo "========== 代理节点列表 =========="
    i=1
    # ============= 修改此处 =============
    echo "$proxies" | jq -r '.[]' | while IFS= read -r proxy; do
        echo "$i. $proxy"
        i=$((i+1))
    done
    echo "==================================="
    read -p "请选择代理节点（输入编号）：" proxy_index
    proxy=$(echo "$proxies" | jq -r ".[$((proxy_index-1))]")
    # ============= 修改结束 =============
    if [[ -n $proxy ]]; then
        # 更新Clash的代理节点设置
        curl -X PUT -s "http://127.0.0.1:9090/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9" -H "Content-Type: application/json" -H "Authorization: Bearer ${secret}" --data "{\"name\":\"$proxy\"}"

        echo "代理节点已更新为：$proxy"
    else
        echo "无效的选择！"
    fi
}

select_proxy
```

```shell
# 创建services文件（需要root用户，这种方式是全局的）
touch /etc/systemd/system/clash.service
# 特别的，如果是用户级别的服务，可以
touch ~/.config/systemd/user/clash.service
```

编辑service内容如下

```text
[Unit]
Description=clash daemon

[Service]
Type=simple
ExecStart=/path/to/your/clash -d /path/to/your/clash-config-dir
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启动、停用clash，但一般不出问题不用执行，只有有问题了可以手动验证一下

```shell
# 手动启动
systemctl --user start clash
# 用户登录时自启
systemctl --user enable clash
# 关闭
systemctl --user stop clash
# 注意，如果是root级别的服务，取消掉--user
```

设置代理打开终端时自动启动（这里因为还要设置代理，所以不能单纯用服务自动启动的办法实现）：
在~/.zshrc中添加如下内容（使用其他bash类似）

```shell
############## clash settings ##########
clashon(){
  systemctl --user start clash
  export http_proxy="http://127.0.0.1:7890"
  export https_proxy="http://127.0.0.1:7890"
  export all_proxy="socks5://127.0.0.1:7891"
  git config --global http.proxy http://127.0.0.1:7890
  git config --global https.proxy http://127.0.0.1:7890
}
clashoff(){
  # 关闭clash的命令
  systemctl --user stop clash
  unset http_proxy
  unset https_proxy
  unset all_proxy
}

# 选择代理节点
clash_select_proxy() {
    bash /path/to/your/select_proxy.sh
}
# 允许局域网访问
clash_allow_lan(){
  curl -X PATCH "http://127.0.0.1:9090/configs" -H "Content-Type: application/json" -H "Authorization: Bearer ${secret}" --data "{\"allow-lan\":true}"
  curl -X GET "http://127.0.0.1:9090/configs"
}

############## clash settings end ##########

```

## docker设置代理

首先明确，系统级别的代理配置无法影响到docker运行，需要分别为dockerd和Container设置代理。

dockerd设置代理：

```shell
mkdir /etc/systemd/system/docker.service.d/
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

写入：

```text
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.0/24"
```

重启服务：

```shell
systemctl daemon-reload
systemctl restart docker
docker info
```

Container设置代理是为了能在运行期间也能够走都代理：

配置`~/.docker/config.json`，注意这里要填写的是本机IP，不能写localhost，因为这是从docker里面访问，除非你已使用的是--host模式启动docker另说：

```text
{
  "proxies": {
    "default": {
      "httpProxy": "http://x.x.x.x:7890",
      "httpsProxy": "http://x.x.x.x:7890",
      "noProxy": "localhost,127.0.0.1"
    }
  }
}
```

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

## GPU机器安装nvidia-smi

首先确保机器中有nvidia显卡

```shell
lspci | grep -i nvidia
```

验证系统是否安装了gcc：gcc --version

若未安装请使用下列命令进行安装必要的包：

```shell
sudo apt install build-essential dkms
```

```shell
sudo apt update
ubuntu-drivers devices # 检查推荐的驱动
sudo ubuntu-drivers autoinstall # 自动安装
sudo reboot
```

## 安装anaconda

```shell
# 注意去官网找最新的
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh
```
