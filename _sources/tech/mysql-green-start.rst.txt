mysql绿色启动方法
========================

下载 `MySQL Linux - Generic 版本 <http://dev.mysql.com/downloads/mysql/>`_ 并解压缩。

根据 ``support-files/my-default.cnf`` 编辑 ``my.conf``

初始化并启动MySQL::

    ./bin/mysqld --initialize  --datadir=/datadir
    ./bin/mysqld --defaults-file=my.conf

