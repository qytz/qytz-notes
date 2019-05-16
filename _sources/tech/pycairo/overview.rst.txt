********
概览
********

.. currentmodule:: cairo

Pycairo 是cairo图形哭的Python语言绑定。

Pycairo 绑定被设计为与cairo的C语言API尽可能的接近，只在某些明显可以以更加 ‘Pythonic’ 化方式实现的地方稍有改变。

Pycairo 绑定的特性：

* 提供一个面向对象的接口。
* 调用 Pycairo_Check_Status()  函数来检查cairo操作的状态，在适当的时候发送异常。
* 提供C API以供其他Python extension使用。

Pycairo 绑定并没有提供cairo_reference(), cairo_destroy(), cairo_surface_reference(), cairo_surface_destroy()
(以及用于Surface和pattern的等价的函数)cairo 的这些C函数，因为对象的构造和销毁由Pycairo来处理。

要使用 pycairo库，请导入::

  import cairo

参考 :ref:`Reference <reference_index>` 了解更详细的信息。

pycairo 的例子请参考pycairo发行代码中的 ‘example’ 目录。
