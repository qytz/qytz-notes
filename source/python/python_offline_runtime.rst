离线环境下Python运行环境配置指南
=====================================

安装并配置 Python 运行环境
--------------------------------
根据需要下载对应的 `Miniconda <http://conda.pydata.org/miniconda.html>`_ 版本并安装。

假定 Miniconda 已经安装到了 [miniconda] 目录。

创建新的Python运行环境并激活::

    $ [miniconda]/bin/conda create -n myenv python
    $ source [miniconda]/bin/activate myenv

在此之后即可使用此 Python 环境进行开发，安装依赖可使用 pip 工具::

    $ pip install sqlalchemy

使用 pip wheel 打包依赖到本地
-------------------------------------

下载依赖包的 wheel 文件::

    $ source [miniconda]/bin/activate myenv
    $ pip wheel -r requirements.txt -w wheelhouse

默认情况下，上述命令会下载 requirements.txt 中每个包的 wheel 包到当前目录的 wheelhouse 文件夹, 包括依赖的依赖。现在你可以把这个 wheelhouse 文件夹打包到你的安装包中。


安装本地依赖包
----------------

首先 `安装并配置 Python 运行环境`_

在你的安装脚本中执行::

    $ source [miniconda]/bin/activate myenv
    $ pip install --use-wheel --no-index --find-links=wheelhouse -r requirements.txt

依赖环境已经安装，现在可以在此环境运行你的程序了。

