======================
简易 git 服务器
======================
简易 gitolite 服务器搭建
==============================
服务器搭建
-------------------------
步骤如下

1. 创建 git 用户

.. code-block:: bash

   sudo adduser git
   su - git

2. 添加 ssh 公钥

.. code-block:: bash

   mkdir .ssh
   cat /tmp/id_rsa.lenny.pub >> ~/.ssh/authorized_keys

3. 在任何 git 用户可读写的位置新建 git 裸仓库

.. code-block:: bash

   mkdir project.git
   cd project.git
   git --bare init

服务器使用
-------------------
远程直接克隆和推送内容

.. code-block:: bash

    git clone git@gitserver:/home/git/project.git
    cd project
    echo "sample git project" README
    git commit -am 'fix for the README file'
    git push origin master



使用 gitolite 搭建 git 服务器
=================================
服务器搭建
---------------

.. code-block:: bash

    apt-get install gitolite3 git-core

安装 gitolite3 会要求输入管理员的 ssh 公钥。

服务器管理
----------------
下载管理仓库
+++++++++++++++++++
Gitolite 使用 gitolite-admin.git 仓库来管理，所以需要抓下来修改、设置（未来所有管理也是如此）。

.. code-block:: bash

    git clone gitolite@gitserver:gitolite-admin
    cd gitolite-admin
    ls
    conf/gitolite.conf # 配置项，配置谁可以读写哪个仓库 Repository。
    keydir # 目录，存放每个帐号的 public key。 放置的文件命名：user1.pub, user2.pub (user1, user2.. 为帐号名称（文件名 = 帐号名）, 建议使用"帐号.pub" 文件名）


新增帐号
+++++++++++++++++++

.. code-block:: bash

    cd gitolite-admin
    cp /tmp/user1.pub keydir/user1.pub # 依照实际帐号命名，不要取 user1, user2
    cp /tmp/user1.pub keydir/user1@machine.pub # 若相同帐号，則使用 user@machine.pub
    cp /tmp/user2.pub keydir/user2.pub
    git add keydir/user1.pub keydir/user1@machine.pub keydir/user2.pub
    git commit -m 'add user1, user1@machine, user2 public key'
    git push

gitolite.conf 配置
++++++++++++++++++++++++++++++++++++

::

    # 取自 2.3.1 授權文件基本語法
    @admin = jiangxin wangsheng

    repo gitolite-admin
    RW+    = jiangxin

    repo ossxp/.+
    C       = @admin
    RW     = @all

    repo testing
    RW+                   =   @admin
    RW      master        =   junio
    RW+     pu            =   junio
    RW      cogito$        =   pasky
    RW      bw/           =   linus
    -                        =   somebody
    RW      tmp/           =   @all
    RW      refs/tags/v[0-9] =   junio

    # 取自 2.3.3 ACL
    repo testing
    RW+   = jiangxin @admin
    RW    = @dev @test
    R      = @all



::

    repo 语法

        repo 語法：《權限》 『零個或多個正規表示式批配的引用』 = <user> [<user> ...]
        每條指令必須指定一個權限，權限可以用下面任何一個權限的關鍵字：C, R, RW, RW+, RWC, RW+C, RWD, RW+D, RWCD, RW+CD
            C : 建立
            R : 讀取
            RW : 讀取 + 寫入
            RW+ : 讀取 + 寫入 + 對 rewind 的 commit 做強制 Push
            RWC : 授權指令定義 regex (regex 定義的 branch、tag 等）, 才可以使用此授權指令。
            RW+C : 同上，C 是允許建立 和 regex 配對的引用 (branch、tag 等）
            RWD : 授權指令中定義 regex (regex 定義的 branch、tag 等）, 才可以使用此授權指令。
            RW+D : 同上，D 是允許刪除 和 regex 配對的引用 (branch、tag 等）
            RWCD : 授權指令中定義 regex (regex 定義的 branch、tag 等）, 才可以使用此授權指令。
            RW+CD : C 是允許建立 和 regex 配對的引用 (branch、tag 等）, D 是允許刪除 和 regex 配對的引用 (branch、tag 等）
            - : 此設定為不能寫入，但是可以讀取
            註：若 regex 不是以 refs/ 開頭，會自動於前面加上 refs/heads/

    群组

        @all 代表所有人的意思
        @myteam user1 user2 : user1, user2 都是屬於 myteam 這個群組

.. note::
    gitolite 配置的应通过 gitolite-admin 仓库修改并提交到服务器，如若手动更改了服务器端的配置，如更改仓库的存储位置（仓库位置为 gitolite 用户的家目录）等，
    需运行 gitolite setup/gl-setup 修复。


gitweb 配置
=================================

.. code-block:: bash

    sudo apt-get install gitweb
    sudo vim /etc/gitweb.conf
        $projectroot = "/home/git/repositories/";
        $projects_list = "/home/git/projects.list";
    sudo mv /etc/apache2/conf.d/gitweb /etc/apache2/conf-available/gitweb.conf
        Options +FollowSymLinks +ExecCGI
    sudo a2enconf gitweb
    sudo a2enmod cgi
    sudo apache2ctl restart

需主意 gitweb 对 git 的 projectroot 和 projects_list 要有权限。
可以设置 gitolite 的掩码：

.. code-block:: bash

    vim /var/lib/gitolite3/.gitolite.rc #$REPO_UMASK = 0027;
    sudo usermod -G gitolite3 www-data
    sudo chmod 640 /val/lib/gitolite2/projects.list

svn 仓库迁移到 git
===================
参考 `迁移 SVN 到 Git Server <http://www.xbc.me/svn-to-git-server/>`_ 及 `迁移 SVN 到 Git Server (git-scm) <http://git-scm.com/book/zh/Git-%E4%B8%8E%E5%85%B6%E4%BB%96%E7%B3%BB%E7%BB%9F-%E8%BF%81%E7%A7%BB%E5%88%B0-Git>`_

引用
===============

1. `Linux 使用 Gitolite 架設 Git Server <http://blog.longwin.com.tw/2011/03/linux-gitolite-git-server-2011/>`_
#. `服务器上的 Git - Gitolite <http://git-scm.com/book/zh/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-Gitolite>`_
#. `How to install gitweb in Ubuntu <http://www.lucidlynx.com/how-to-install-gitweb-in-ubuntu/>`_
