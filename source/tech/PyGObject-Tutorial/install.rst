.. _install:

安装
============
在开始我们真正的编程前，需要先设置好 `PyGObject`_ 的依赖。PyGObject是一个Python模块，可以让开发者使用Python调用基于GObject的庞大类库，比如GTK+。
它只支持GTK+3及以上的版本。如果你想在你要编写的程序中使用GTK+2，请绕行使用 `PyGTK`_ 代替。

依赖
------------

* GTK+3

* Python 2 (2.6或更高) 或 Python 3 (3.1或更高)

* gobject-introspection

预编译的二进制包
---------------------
最近版本的PyGObject及其依赖包已经被几乎所有的Linux发行版打包
。因此，如果你使用Linux的话（这貌似是废话哎），你可以直接从你的发行版的官方仓库安装这些包。

从源代码安装
----------------------
从源代码安装PyGObject的最简单方法就是使用 `JHBuild`_ 。其就是为了简化源码包的编译及检测
哪些依赖包要以怎样的顺序来编译而设计的。要安装JHBuild，请移步至： `JHBuild manual`_ 。
一旦你成功的安装了JHBuild，从 [#]_ 下载最新的配置文件，并将其拷贝至JHBuild的模块目录，
重命名以 `.modules` 后缀结尾。然后将示例文件—— `sample-tarball.jhbuildrc` 拷贝至 `~/.jhbuildrc` 。
如果你完成了上述步骤，测试下你的编译环境是否可以正常运行::

    $ jhbuild sanitycheck

如果一切正常，将会打印出现在你的系统中缺失的库和程序。你应该使用你发发行版的软件仓库来安装这些东西。
不同发行版的的 `包名称列表 <http://live.gnome.org/JhbuildDependencies>`_ 在GNOME wiki上面有维护。
完成之后再次运行该命令以确保需要的包都已经安装。执行下面的命令就可以编译PyGObject及其所有的依赖了::

    $ jhbuild build pygobject

最后，你可能也会想要从源代码安装GTK+：（呃，谁会那么傻呢。。。）::

    $ jhbuild build gtk+

要打开一个与JHBuild相同环境变量的shell，请执行：（真麻烦）::

    $ jhbuild shell

Ps：哎，这年头应该没有人真的从源代码来编译这个玩意吧，故以上代码未验证，翻译页可能不准确，请见谅。

.. _PyGObject: https://live.gnome.org/PyGObject
.. _PyGTK: http://www.pygtk.org
.. _JHBuild: https://live.gnome.org/Jhbuild
.. _JHBuild manual: http://library.gnome.org/devel/jhbuild/unstable/

.. [#] http://download.gnome.org/teams/releng/
