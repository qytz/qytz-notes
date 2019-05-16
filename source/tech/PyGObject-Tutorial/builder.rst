Glade and Gtk.Builder
=====================
:class:`Gtk.Builder` 可以让你不用写一行的代码就可以设计界面。这是通过使用一个
XML文件来描述界面然后在运行时通过Builder类加载此XML描述文件并自动创建对象来实现的。
`Glade <http://glade.gnome.org/>`_ 应用可以使你不需要手动编写XML文件而以一种
WYSIWYG(所见即所得)的方式来设计界面。

这种方式有很多优点：

* 写更少的代码。
* UI 更加容易改变，因此可以改进UI。
* 没有编程经验的设计师可以创建并编辑UI。
* UI的描述与正在使用的编程语言相互独立。

仍然需要用户对界面修改的代码，但是 :class:`Gtk.Builder` 允许你集中注意力实现程序的功能。

创建并加载 .glade 文件
------------------------------------
首先你需要下载并安装Glade。有 `很多关于Glade的教程 <https://live.gnome.org/Glade/Tutorials>`_ ，
因此这里不再详细介绍。让我们开始创建一个带有一个按钮的窗口并保存其为 *example.glade* 。
最终的XML文件看起来像下面这样：

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <interface>
      <!-- interface-requires gtk+ 3.0 -->
      <object class="GtkWindow" id="window1">
        <property name="can_focus">False</property>
        <child>
          <object class="GtkButton" id="button1">
            <property name="label" translatable="yes">button</property>
            <property name="use_action_appearance">False</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="use_action_appearance">False</property>
          </object>
        </child>
      </object>
    </interface>

要在Python中加载这个文件我们需要一个 :class:`Gtk.Builder` 对象。

.. code-block:: python

    builder = Gtk.Builder()
    builder.add_from_file("example.glade")

第二行加载所有 *example.glade* 定义的对象到Buildeer对象中。

当然也可以只加载一部分对象。下载的代码只加载了tuple中指定的对象(及其孩子对象)。

.. code-block:: python

    # we don't really have two buttons here, this is just an example
    builder.add_objects_from_file("example.glade", ("button1", "button2"))

这两种方法也可以在字符串中加载对象。他们对应的函数为
:meth:`Gtk.Builder.add_from_string` 和 :meth:`Gtk.Builder.add_objects_from_string` ，
他们从参数中取得XML字符串而不是文件名。

访问控件
-----------------
现在我们想要显示的窗口和按钮都加载进来了。因此要在该窗口上调用
:meth:`Gtk.Window.show_all` 方法，但是我们如何访问我们的对象呢？

.. code-block:: python

    window = builder.get_object("window1")
    window.show_all()

每一个控件都可以通过 :meth:`Gtk.Builder.get_object` 方法和控件的 *id* 来获取。哈哈，真简单。

当然也可以加载所有对象到一个列表中

.. code-block:: python

    builder.get_objects()

连接信号
------------------
Glade 也使得定义你想要连接到你代码里的函数的信号成为可能，并却这不需要从builder
加载每一个对象并且手动去连接信号。要做的第一件事就是在Glade中声明信号的名字。
例子中我们在按钮按下时关闭窗口，所以我们给窗口的 "delete-event" 信号设置处理函数
"onDeleteWindow" ， "pressed" 信号设置处理函数 "onButtonPressed" 。
现在XML文件看起来像下面这个样子：

.. literalinclude:: examples/builder_example.glade
	:language: xml

现在我们要在代码中定义处理函数。 *onDeleteWindow* 应该简单地调用 :meth:`Gtk.main_quit` 。
当按钮按下时我们可能想要打印字符串 "Hello World!" ，因此我们定义的函数看起来像：

.. code-block:: python

    def hello(button):
        print "Hello World!"

接下来，我们要连接信号和处理函数。最简单的方法是定义一个带有名字到处理函数的映射
*dict* 并传递给 :meth:`Gtk.Builder.connect_signals` 方法。

.. code-block:: python

    handlers = {
        "onDeleteWindow": Gtk.main_quit,
        "onButtonPressed": hello
    }
    builder.connect_signals(handlers)

一种可选的方法是创建一个包含要调用的函数的类，在我们的例子中最终的代码片段如下：

.. literalinclude:: examples/builder_example.py
    :linenos:
    :lines: 3-12

Builder 对象
---------------
.. class:: Gtk.Builder

    .. method:: add_from_file(filename)

        加载并解析给定的文件并合并到builder当前的内容。

    .. method:: add_from_string(string)

        解析给定的字符串并合并到builder当前的内容。

    .. method:: add_objects_from_file(filename, object_ids)

        与 :meth:`Gtk.Builder.add_from_file` 一样，但是只加载 *object_ids* 列表给定的对象。

    .. method:: add_objects_from_string(filename, object_ids)

        与 :meth:`Gtk.Builder.add_from_string` 一样，但是只加载 *object_ids* 列表指定的对象。

    .. method:: get_object(object_id)

        从由builder加载的对象中获取 *object_id* 指定的控件。

    .. method:: get_objects()

        返回所有加载的对象。

    .. method:: connect_signals(handler_object)

        连接信号到 *handler_object* 指定的方法。 *handler_object* 可以为任何包含
        界面描述文件中指定的信号处理函数名字键或属性的对象，例如一个类或者字典。

Example
-------
The final code of the example

.. literalinclude:: examples/builder_example.py
    :linenos:
