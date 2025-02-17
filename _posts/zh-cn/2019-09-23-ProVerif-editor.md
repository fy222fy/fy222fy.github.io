---
layout: post
title: Windows系统如何安装ProVerif Editor
date: 2024-05-01 00:32:13
description: this is what included tabs in a post could look like
tags: formatting code
categories: sample-posts
tabs: true
---

@[TOC](Windows系统如何安装ProVerif Editor)

ProVerif是一个强大的协议形式化分析工具，它可以根据输入的pv文件自动分析协议。为了方便研究者编辑应用PI演算，Joeri de Ruiter利用Python语言开发了一款ProVerif编辑器--**ProVerif editor**。但是,这款工具最近一次的更新已经是2013年4月了，它是用Python2开发的，并且使用的相关库都是比较老版本的，在安装过程中，出了很多错误，所以在这里记录一下如何让这个工具能正常地跑起来。本文参考了[为Python添加GTK+库：pygtk（windows下安装pygtk）](http://blog.qqzzz.net/?post=34)和 [Making pygtksourceview work in windows](https://stackoverflow.com/questions/2968273/making-pygtksourceview-work-in-windows)两篇文章。

# 工具下载

ProVerif工具下载链接: [https://prosecco.gforge.inria.fr/personal/bblanche/proverif/](https://prosecco.gforge.inria.fr/personal/bblanche/proverif/).
ProVerif editor工具下载链接：[https://sourceforge.net/projects/proverifeditor/](https://sourceforge.net/projects/proverifeditor/).

# 工具运行需求

解压proverif_editor，找到README文件，可以看到ProVerif Editor的需求。

1. ProVerif
2. Python(>=2.6)
3. PyGTK2
4. PyGTKSourceView2 (README中这里写错了)

## Python

在Python的官网中下载大于2.6版本小于3版本的Python。我最后选择了Python2.7.8，下载地址：[https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi](https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi). 注意一定要下载32位的Python，因为后面的PyGtk只有32位版本的，与64位的Python不兼容。

## PyGTK2

### GTK安装

在下载PyGTK前，确保先下载GTK，我下载的是GTK2.24.10_win32，下载地址：[http://gemmei.ftp.acc.umu.se/pub/gnome/binaries/win32/gtk+/2.24/gtk+-bundle_2.24.10-20120208_win32.zip](http://gemmei.ftp.acc.umu.se/pub/gnome/binaries/win32/gtk+/2.24/gtk+-bundle_2.24.10-20120208_win32.zip).

还需要下载PyCairo，和PyGObject。
PyCairo下载地址：[http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/1.8/pycairo-1.8.10.win32-py2.7.msi](http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/1.8/pycairo-1.8.10.win32-py2.7.msi).
PyGObject下载地址：[http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/2.26/pygobject-2.26.0-1.win32-py2.7.msi](http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/2.26/pygobject-2.26.0-1.win32-py2.7.msi).
下载后直接打开安装，会自动找到Python2.7的目录。

将GTK安装包解压，并将文件的bin目录添加到系统的环境变量中。之后进行测试，在cmd下执行pkg-config --cflags gtk+-2.0 ，看是否有报错信息，如果没有，通过命令gtk-demo来验证是否安装正确，安装正确会跳出一个窗口。

Windows下正常运行PyGTK还需要GTK+ for Windows Runtime Environment，下载地址：[http://sourceforge.net/projects/gtk-win/](http://sourceforge.net/projects/gtk-win/).

### PyGTK安装

我下载的是PyGTK2.24.0.win32-py2.7，下载地址：[http://ftp.gnome.org/pub/gnome/binaries/win32/pygtk/2.24/pygtk-2.24.0.win32-py2.7.msi](http://ftp.gnome.org/pub/gnome/binaries/win32/pygtk/2.24/pygtk-2.24.0.win32-py2.7.msi).下载后直接点击安装，它会自己寻找到你的Python2.7目录。

## PyGTKSourceView2

我下载的是PyGTKSourceView2.10.1.win32-py2.7，下载地址：[http://ftp.gnome.org/pub/gnome/binaries/win32/gtksourceview/2.10/gtksourceview-2.10.0.zip](http://ftp.gnome.org/pub/gnome/binaries/win32/gtksourceview/2.10/gtksourceview-2.10.0.zip).
下载后将压缩包解（为方便可以加压到Python目录下），然后将文件的bin目录添加到环境变量中。

正当我觉得一切任务完成后，在打开ProVerif editor时报错:**DLL load failed: 找不到指定的模块**，但是报错又不告诉我找不到什么模块，于是我只好一步一步研究。

最后我找到了PyGTKSourceView2.10的源代码，发现想要运行PyGTKSourceView2，需要glib-2.14.x, GTK+-2.12.x and libxml2 2.5.x. 于是我又去找到了这glib和libxml这两个dll进行安装。
glib下载地址：[http://ftp.acc.umu.se/pub/gnome/binaries/win32/glib/2.14/glib-2.14.6.zip](http://ftp.acc.umu.se/pub/gnome/binaries/win32/glib/2.14/glib-2.14.6.zip).
libxml下载地址：[http://ftp.acc.umu.se/pub/gnome/binaries/win32/dependencies/libxml2_2.7.7-1_win32.zip](http://ftp.acc.umu.se/pub/gnome/binaries/win32/dependencies/libxml2_2.7.7-1_win32.zip).
下载后把这两个压缩包解压，然后将它们的bin目录（其中的dll目录）添加到环境变量中。

这样python就能正常使用gtk了，最后在使用的过程中，ProVerif editor种的editor.py无法正确导入parser.py，可能是因为和Python本身的包重名了，如果遇到这个问题，改一下parser.py的文件名称和对应的editor.py的导入名称就可以了。
