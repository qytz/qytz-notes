.. _exceptions:

**********
Exceptions
**********

.. currentmodule:: cairo

当一个cairo函数或方法调用失败时会触发异常。
I/O错误会触发IOError，内存错误会触发MemoryError，其他的错误会触发cairo.Error。

cairo.Error()
=============

.. exception:: cairo.Error

   当一个cairo对象返回一个错误的状态值时触发本异常。
