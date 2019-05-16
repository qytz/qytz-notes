.. _paths:

*****
Paths
*****

.. currentmodule:: cairo

class Path()
============

.. class:: Path()

   *Path* 不能被直接实例化，只能通过调用
   :meth:`Context.copy_path` 和 :meth:`Context.copy_path_flat` 创建。

   str(path) 会列出路径的所有元素。

   参考 :ref:`PATH attributes <constants_PATH>`

   Path 是一个迭代器。

   例子用法参考 examples/warpedtext.py 。
