***
FAQ
***

.. currentmodule:: cairo


Pycairo FAQ - Frequently Asked Questions
========================================

Q: 我可以子类化 Pycairo 的类吗？

A: cairo 的C库，并不是一个面向对象的库，所有 Python绑定永远都不可能提供真正的面向对象的接口。
如果采用一个很长的模块函数列表的方式来实现绑定，可能最准确的代表了C库的形式。
但是Pycairo（以及绝大多数cairo其他语言的绑定？）选择了实现Context、Surface、Pattern等这几个类的
方式来实现。这样做的优点是按照cairo库中类似的函数按照不同的类分成为了几组，缺点是产生了cairo是一个
面向对象的库的错觉，然后开发者可能就会去尝试创建子类来覆盖criro的一些方法。
而事实上没有方法可以被覆盖，只有不能被覆盖的cairo方法。

cario 文档的附录A "给cairo创建一个语言绑定"的 "内存管理" 章节描述了为什么从Surface派生会产生问题，
因此最好避免这样使用。

cairo.Context 可以被子类化。
所有其他的 Pycairo 子类都不能被子类化。


Q: pycairo如何与numpy一起使用？

A: 参见 test/isurface_create_for_data2.py


Q: pycairo如何与pygame一起使用？

A: 参见 test/pygame-test1.py
        test/pygame-test2.py
