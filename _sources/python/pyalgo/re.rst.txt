正则模块
==========

正则模块的用法
------------------
Python 正则模块的用法非常简单，总结起来就是两种用法和几个函数。

可以导入 `re` 模块后直接使用 `re.match` 和 `re.search` 进行匹配

.. code:: python

    In [1]: import re

    In [2]: orig_str = '123abcdef'

    In [3]: match_str = 'abc'

    In [4]: re.match(match_str, orig_str) is None
    Out[4]: True

    In [5]: re.search(match_str, orig_str) is None
    Out[5]: False

    In [6]: match = re.search(match_str, orig_str)

    In [7]: match.start()
    Out[7]: 3

    In [8]: match.end()
    Out[8]: 6

    In [9]: orig_str[match.start():match.end()]
    Out[9]: 'abc'

    In [10]: 

    In [11]: match_str = '(abc)'

    In [12]: match = re.search(match_str, orig_str)

    In [13]: match.group()
    Out[13]: 'abc'

    In [14]: match.groups()
    Out[14]: ('abc',)

也可可以导入 `re` 模块后使用 `re.compile` 后再进行匹配

.. code:: python

    In [1]: import re

    In [2]: orig_str = '123abcdef'

    In [3]: match_str = '(abc)'

    In [4]: pattern = re.compile(match_str)

    In [5]: pattern.search(orig_str)
    Out[5]: <_sre.SRE_Match object; span=(3, 6), match='abc'>

    In [6]: ret = pattern.search(orig_str)

    In [7]: ret.start()
    Out[7]: 3

    In [8]: ret.end()
    Out[8]: 6


    In [9]: 

    In [9]: ret = pattern.match(orig_str)

    In [10]: ret is None
    Out[10]: True


如何写出满足需求的正则表达式
--------------------------------

参考 `Python正则表达式指南 <http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html>`_

