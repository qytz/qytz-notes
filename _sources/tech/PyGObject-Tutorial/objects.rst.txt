.. _objects:

对象系统
==========

GObject 是基础类型提供了Gtk+对象系统需要的所有属性和方法。 :class:`GObject.GObject`
提供了构造和析构对象的方法，属性访问方法和信号支持。

本节将要介绍Python实现的GObject一些重要的方面。

从GObject.GObject继承
----------------------------

一个原生的GObject可以通过 :class:`GObject.GObject` 访问，但通常很少直接实例化，而是
使用继承后的类。 :class:`Gtk.Widget` 就是一个继承自 :class:`GObject.GObject` 的类。
创建一个继承类来创建一个新的如设置对话框的新控件通常很有趣。

要从 :class:`GObject.GObject` 继承，你必须在你的构造函数中调用
:meth:`GObject.GObject.__init__` ，例如如果你的类继承自 :class:`Gtk.Button` ，则必须
调用 :func:`Gtk.Button.__init__` ， 就像下面这样。

.. code-block:: python

    from gi.repository import GObject

    class MyObject(GObject.GObject):

        def __init__(self):
            GObject.GObject.__init__(self)


信号
-------

信号可以随意的连接到程序相关的事件，可以有任意多个收听者。例如， 在GTK+里面，每一个
用户事件(按键或鼠标移动) 从X server接收后产生一个GTK+事件在给的的对象实例上触发信号。

每一个信号都与其可以触发的类型一起在类型系统里面注册：当类型的使用者注册信号触发
时的回调函数时，要链接信号到给定类型的实例。

接收信号
^^^^^^^^^^^^^^^

参考 :ref:`signals`

创建新的信号
^^^^^^^^^^^^^^^^^^

可以通过添加信号到 :attr:`GObject.GObject.__gsignals__` 字典中创建新的信号。

当创建新的信号时也可以定义一个处理方法，该方法会在每次信号触发时调用，叫做 do_signal_name 。

.. code-block:: python

    class MyObject(GObject.GObject):
        __gsignals__ = {
            'my_signal': (GObject.SIGNAL_RUN_FIRST, None,
                          (int,))
        }

        def do_my_signal(self, arg):
            print "class method for `my_signal' called with argument", arg

:const:`GObject.SIGNAL_RUN_FIRST` 指示在信号触发的第一阶段调用对象方法
(此处:meth:`do_my_signal`)。也可以设置为 :const:`GObject.SIGNAL_RUN_LAST` (
方法在信号触发的第三阶段调用)和 :const:`GObject.SIGNAL_RUN_CLEANUP` (在信号触发
的最后一个阶段调用)。

第二个参数， ``None`` 指示信号的返回类型，通常为 ``None`` 。

``(int,)`` 指示信号的参数，此处信号只接收一个参数，类型为 int 。参数类型列表必须
以逗号结束。

信号可以使用 :meth:`GObject.GObject.emit` 触发。

.. code-block:: python

    my_obj.emit("my_signal", 42) # emit the signal "my_signal", with the
                                 # argument 42

属性
----------
GObject一个很好的特性就是其对于对象属性的get/set方法。每一个继承自 :class:`GObject.GObject`
的类都可以定义新的属性，每一个属性作为一个类型永远不会改变(例如 str, float, int等)。
例如 :class:`Gtk.Button` 的 "label" 属性包含了按钮的文本。

使用已有的属性
^^^^^^^^^^^^^^^^^^^^^^^

:class:`GObject.GObject` 提供了多个很有用的函数来管理已有的属性，
:func:`GObject.GObject.get_property` 和 :func:`GObject.GObject.set_property` 。

一些属性也有他们相应的函数，叫做getter和setter。对于按钮的 "label" 属性，有两个函数
来获取和设置该属性， :func:`Gtk.Button.get_label` 和 :func:`Gtk.Button.set_label` 。

创建新的属性
^^^^^^^^^^^^^^^^^^^^^

属性通过名字和类型定义，即使python是动态类型的，一旦定义你也不能改变属性的类型。
属性可以通过 :func:`GObject.property` 创建。

.. code-block:: python

    from gi.repository import GObject

    class MyObject(GObject.GObject):

        foo = GObject.property(type=str, default='bar')
        property_float = GObject.property(type=float)
        def __init__(self):
            GObject.GObject.__init__(self)

如果你想让某些属性只读不可写，属性也可以为只读的。要这样做，你可以给属性定义添加
一些标志flags，来控制读写权限。标志有 :const:`GObject.PARAM_READABLE` (只能通过
外部代码读取)， :const:`GObject.PARAM_WRITABLE` (只可写)，
:const:`GObject.PARAM_READWRITE` (public):

.. there is also construct things, but they
.. doesn't seem to be functional in python

.. code-block:: python

    foo = GObject.property(type=str, flags = GObject.PARAM_READABLE) # won't be writable
    bar = GObject.property(type=str, flags = GObject.PARAM_WRITABLE) # won't be readable


你也可以通过 :func:`GObject.property` 与函数修饰符创建新的函数来定义只读属性。

.. code-block:: python

    from gi.repository import GObject

    class MyObject(GObject.GObject):

        def __init__(self):
            GObject.GObject.__init__(self)

        @GObject.property
        def readonly(self):
            return 'This is read-only.'

你可以使用以下代码获取该属性：

.. code-block:: python

    my_object = MyObject()
    print my_object.readonly
    print my_object.get_property("readonly")

也有定义数值类型属性的最大值和最小值的方法，需要使用更加复杂的形式：

.. code-block:: python

    from gi.repository import GObject

    class MyObject(GObject.GObject):

        __gproperties__ = {
            "int-prop": (int, # type
                         "integer prop", # nick
                         "A property that contains an integer", # blurb
                         1, # min
                         5, # max
                         2, # default
                         GObject.PARAM_READWRITE # flags
                        ),
        }

        def __init__(self):
            GObject.GObject.__init__(self)
            self.int_prop = 2

        def do_get_property(self, prop):
            if prop.name == 'int-prop':
                return self.int_prop
            else:
                raise AttributeError, 'unknown property %s' % prop.name

        def do_set_property(self, prop, value):
            if prop.name == 'int-prop':
                self.int_prop = value
            else:
                raise AttributeError, 'unknown property %s' % prop.name

属性必须通过 :attr:`GObject.GObject.__gproperties__` 字典定义，并通过
do_get_property 和 do_set_property 来处理。

监视属性
^^^^^^^^^^^^^^^^

当属性被修改时，会触发一个信号， "notify::property_name" ：

.. code-block:: python

    my_object = MyObject()

    def on_notify_foo(obj, gparamstring):
        print "foo changed"

    my_object.connect("notify::foo", on_notify_foo)

    my_object.set_property("foo", "bar") # on_notify_foo will be called

API
---

.. class:: GObject.GObject

    .. method:: get_property(property_name)

        获取属性的值。

    .. method:: set_property(property_name, value)

        设置属性 *property_name* 的值为 *value* 。

    .. method:: emit(signal_name, ...)

        触发信号 *signal_name* 。信号的参数必须在后面传递，例如，如果你的信号类型
        为 ``(int,)`` ，则要像下面这样触发::

            self.emit(signal_name, 42)

    .. method:: freeze_notify()

        本函数会冻结所有 "notify::" 信号(这些信号会在属性改变时触发) 指导
        :meth:`thaw_notify` 被调用。

        建议调用 :meth:`freeze_notify` 时使用 *with* 语句，这样可以确保 :meth:`thaw_notify`
        在语句块的最后被调用::

            with an_object.freeze_notify():
                # Do your work here
                ...

    .. method:: thaw_notify()

        解冻所有的被 :meth:`freeze_notify` 冻结的 "notify::" 信号。

        建议不要明确地调用 :meth:`thaw_notify` 而是 *with* 语句与
        :meth:`freeze_notify` 一起使用。

    .. method:: handler_block(handler_id)

        阻塞实例的处理函数 *handler_id* 因此在任何信号触发之时都不会被调用，直到
        :meth:`handler_unblock` 被调用。因此 "阻塞" 一个信号处理函数意味着临时
        关闭它，信号处理函数必须与之前阻塞次数相同的取消阻塞才能被再次激活。

        建议 :meth:`handler_block` 与 *with* 语句一起使用，这样会在语句块的最后
        隐式调用 :meth:`handler_unblock` ::

            with an_object.handler_block(handler_id):
                # Do your work here
                ...

    .. method:: handler_unblock(handler_id)

        取消 :meth:`handler_block` 的效果。阻塞后的处理函数会在信号被触发时略过，
        并且直到取消阻塞相同次数之前不会被调用。

        建议不要直接调用 :meth:`handler_unblock` 而是与 *with* 语句一起使用
        :meth:`handler_block` 。

    .. attribute:: __gsignals__

        一个继承类可以定义新信号的字典。

        字典中的每一个元素都是一个新的信号。key为信号的名字，值为一个元组，如下::

            (GObject.SIGNAL_RUN_FIRST, None, (int,))

        :const:`GObject.SIGNAL_RUN_FIRST` 可以被替换为
        :const:`GObject.SIGNAL_RUN_LAST` 或者 :const:`GObject.SIGNAL_RUN_CLEANUP` 。
        ``None`` 为信号的返回类型。 ``(int,)`` 为参数的列表，必须以逗号结尾。

    .. attribute:: __gproperties__

        .. based on http://www.pygtk.org/articles/subclassing-gobject/sub-classing-gobject-in-python.htm

        :attr:`__gproperties__` 字典是一个可以定义你的对象属性的属性。这并不是建议
        的方式定义新属性，上面提到的方法更加的简洁。本方法的优点是可以对属性作更多
        的设置，像数值类型的最大值与最小值之类。

        key 为属性的名字。

        value 为描述属性的元组。
        元组中元素的数目依赖于第一个元素，但一般至少都会包含下面的元素。

            第一个元素为属性的类型(例如 ``int``, ``float`` 等)。

            第二个元素是属性的小名(昵称)，即对属性简短描述的字符串。这通常用于有
            很强内省能力的程序，像GUI builder `Glade`_ 。

            第三个是属性的描述或导语，即另一个更长的，描述属性的字符串。也是给
            `Glade`_ 及类似程序使用的。

            最后一个为属性的标志flags: ::const:`GObject.PARAM_READABLE` ，
            ::const::`GObject.PARAM_WRITABLE`， :const:`GObject.PARAM_READWRITE` 。
            稍后我们会看到，这并不见得是第四个参数。

        元组的长度依赖于属性的类型(元组的地一个元素)。具体包括下面的情形：

            如果类型为 ``bool`` 或者 ``str`` ，第四个元素为属性的默认值。

            如果类型为 ``int`` 或者 ``float`` ，第四个元素是可接收的最小值，第五个
            为可接收的最大值，第六个为其默认值。

            如果类型不是上面这些，则没有额外的元素。


.. attribute:: GObject.SIGNAL_RUN_FIRST

    在信号触发第一阶段调用处理方法。

.. attribute:: GObject.SIGNAL_RUN_LAST

    在信号触发第三阶段调用处理方法。

.. attribute:: GObject.SIGNAL_RUN_CLEANUP

    在信号触发最后一个阶段调用处理方法。

.. attribute:: GObject.PARAM_READABLE

    属性只读。

.. attribute:: GObject.PARAM_WRITABLE

    属性只写。

.. attribute:: GObject.PARAM_READWRITE

    属性可读可写。

.. _Glade: http://glade.gnome.org/
