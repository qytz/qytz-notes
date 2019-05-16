.. _basics:

基础知识
=========
在这一章我们来介绍GTK+中最重要的方面。



.. _signals:

主循环与信号
---------------------
跟绝大多数的GUI工具包一样，GTK+采用了一个事件驱动的编程模型。当用户什么也不做时，
GTK+就在主循环里等着输入信息，如果用户执行了某个动作，比如点了下鼠标，主循环马上“醒来”并将事件投递给GTK+。

当窗口部件收到一个事件时，他们通常会触发一个或多个信号。信号就会通知你的程序说 “某些有意思的事情发生，你赶紧来看看吧” ，
怎么通知呢，当然是调用你你连接到信号上的函数了。这个函数就是通常所说的 *回调函数了* 。当你的回调函数被调用，
你一般会做些操作，比如当一个“打开”按钮“被点击时你一般会打开一个文件选择对话框。
回调函数执行结束后GTK+就返回到主循环继续等待更多的用户输入了。


通常的例子类似于这个样子：

.. code-block:: python

    handler_id = widget.connect("event", callback, data)

首先， *widget* 是一个我们之前创建的窗口部件的实例。
第二，event就是我们感兴趣的事件，每个窗口部件都有其自己的事件。例如，按钮的 ”clicked“ 事件，意思是按钮被按下时信号就被触发了。
第三， *callback* 参数就是回调函数的名字了，其包含相关信号被触发时要执行的代码。
最后， *data* 参数包含任何你想传递给回调函数的数据。但是，这个参数完全是可选的，如果你不需要你完全可以忽略。

这个函数返回一个信号-回调函数的id，当你想断开信号与回调函数的连接时会用到这个id。断开后将要触发及正在触发的该信号都不会再调用该回调函数了。

.. code-block:: python

    widget.disconnect(handler_id)

几乎所有的应用程序都会将 “delete-event” 信号与顶层窗口连接。如果用户关闭顶层窗口时该信号就会被触发。
默认的处理方法只是销毁窗口，但是并不终止程序。将 “delete-event” 与 :func:`Gtk.main_quit` 连接会达到想要的要求。

.. code-block:: python

    window.connect("delete-event", Gtk.main_quit)

调用 :func:`Gtk.main_quit` 使 :func:`Gtk.main` 中的主循环返回。

属性
----------
属性描述了窗口不见的配置和状态信息。每一个窗口部件都有其不同的属性。
例如，一个按钮有 "label" 属性，该属性包含一个在按钮内部显示的label部件的文本。
当创建该窗口部件的实例时，你可以通过关键字参数指定这些属性的名字和值。
要创建一个标签，25度角并且右对齐的显示“Hello World”：

.. code-block:: python

    label = Gtk.Label(label="Hello World", angle=25, halign=Gtk.Align.END)

当然，这与下面的代码是等价的：

.. code-block:: python

    label = Gtk.Label()
    label.set_label("Hello World")
    label.set_angle(25)
    label.set_halign(Gtk.Align.END)

除了使用这些get_xxx和set_xxx外你也可以使用 ``widget.get_property("prop-name")`` 和
``widget.set_property("prop-name", value)`` 来获取和设置属性。
PS：测试了下，显示真的是25度角倾斜的文本，真的很好玩，哈哈～～

