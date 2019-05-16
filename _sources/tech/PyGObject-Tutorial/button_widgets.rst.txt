按钮控件
==============

按钮
------

按钮控件是另一个经常使用的控件。按钮通常会添加一个当点击按钮时要调用的函数。

:class:`Gtk.Button` 按钮控件可以包含任何有效的子控件，即可以包含绝大多数的其他标准的
:class:`Gtk.Widget` 控件。最常会添加的子控件是 :class:`Gtk.Label` 。

通常，你想要连接一个按钮的 "clicked" 信号，该信号当你按下并释放鼠标按钮时会触发。

按钮对象
^^^^^^^^^^^^^^
.. class:: Gtk.Button([label[, stock[, use_underline]]])

    如果lable不是 ``None`` ，会创建一个带有 :class:`Gtk.Label` 的 :class:`Gtk.Button` 按钮，
    标签会包含给定的文本。

    如果 *stock* 不为 ``None`` ，创建的按钮包含 :ref:`stock item <stock-items>` 的图像和文本。

    如果 *use_underline* 为 ``True``, 则label中的下划线后面的字符为助记符加速键。

    .. method:: set_label(label)

    设置按钮标签的内容为 *label* 。

    .. method:: set_use_underline(use_underline)

    如果为 *True* ，按钮标签文本中的下划线预示着下一个字符用于助记符加速键。

例子
^^^^^^^

.. image:: images/button_example.png

.. literalinclude:: examples/button_example.py
    :linenos:

ToggleButton
------------

:class:`Gtk.ToggleButton` 与 :class:`Gtk.Button` 非常类似，但是当点击后，
Toggle按钮保持激活状态，知道再次点击。当按钮的状态改变时， "toggled" 信号会被触发。

要获得 :class:`Gtk.ToggleButton` 的状态，我们可以调用 :meth:`Gtk.ToggleButton.get_active` 方法，
如果Toggle按钮处于按下状态，函数返回 ``True`` 。
当然你也可以设置Toggle按钮的状态——通过 :meth:`Gtk.ToggleButton.set_active` 方法。
如果你这样做了，并且Toggle按钮的状态变了，那么 "toggle" 信号会被触发。

ToggleButton 对象
^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.ToggleButton([label[, stock[,use_underline]]])

    参数与 :class:`Gtk.Button` 的构造函数一样。

    .. method:: get_active()

    返回Toggle按钮当前的状态。如果按钮处于按下状态返回 ``True`` ，否则返回 ``False`` 。

    .. method:: set_active(is_active)

    设置Toggle按钮的状态，如果想设置按钮为按下状态则传递 ``True`` ，否则传递``False`` 。
    会导致 "toggle" 信号被触发。

例子
^^^^^^^

.. image:: images/togglebutton_example.png

.. literalinclude:: examples/togglebutton_example.py
    :linenos:

CheckButton（复选按钮）
------------------------
:class:`Gtk.CheckButton` 继承自 :class:`Gtk.ToggleButton` 。唯一的不同是
:class:`Gtk.CheckButton` 外观。 :class:`Gtk.CheckButton` 会在
:class:`Gtk.ToggleButton` 的旁边放置一个分离的控件——通常是一个 :class:`Gtk.Label` 。
"toggled" 信号， :meth:`Gtk.ToggleButton.set_active` 与
:meth:`Gtk.ToggleButton.get_active` 则继承过来了。

CheckButton 对象
^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CheckButton([label[, stock[, use_underline]]])

    参数与 :class:`Gtk.Button` 同。

RadioButton（单选按钮）
-----------------------
与复选按钮一样，单选按钮也是继承自 :class:`Gtk.ToggleButton` ，但是单选按钮
按照组的方式来工作，并且在组中只有一个 :class:`Gtk.RadioButton` 可以被选中。
因此，:class:`Gtk.RadioButton` 是一种让用户从很多选项中选择一个的方法。

单选按钮Radio buttons可以使用以下任何一个静态函数创建：
:meth:`Gtk.RadioButton.new_from_widget` ，
:meth:`Gtk.RadioButton.new_with_label_from_widget` 或者
:meth:`Gtk.RadioButton.new_with_mnemonic_from_widget` 。
一个组中第一个radio button创建时 *group* 参数传递 ``None`` ，在随后的调用中，
你想要将此按钮加入的组应该作为参数传递。

当第一次运行时，组内的第一个radio按钮会是激活状态的。可以通过
:meth:`Gtk.ToggleButton.set_active` 传递 ``True`` 来修改。

在创建后改变 :class:`Gtk.RadioButton` 控件的分组信息可以通过调用
:meth:`Gtk.RadioButton.join_group` 来实现。

RadioButton 对象
^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.RadioButton

    .. staticmethod:: new_from_widget(group)

        创建一个新的 :class:`Gtk.RadioButton` ，将其添加到与 *group* 控件同一组中。
        如果 *group* 为 ``None`` ，会创建一个新的组。

    .. staticmethod:: new_with_label_from_widget(group, label)

        创建一个 :class:`Gtk.RadioButton` 。标签控件内的文本会被设置为 *lable* 。
        *group* 参数与 :meth:`new_from_widget` 相同。

    .. staticmethod:: new_with_mnemonic_from_widget(group, label)

        与 :meth:`new_with_label_from_widget` 相同，但是 *label* 中的下划线会被解析为按钮的助记符。

    .. method:: join_group(group)

        将radio button加入到另一个 :class:`Gtk.RadioButton` 对象的组中。

Example
^^^^^^^

.. image:: images/radiobutton_example.png

.. literalinclude:: examples/radiobutton_example.py
    :linenos:

LinkButton
----------
:class:`Gtk.LinkButton` 是带有链接的 :class:`Gtk.Button` 。与浏览器中使用的链接类似——
当点击时会触发一个动作，当要快速的链接到一个资源时很有用。

绑定到 :class:`Gtk.LinkButton` 的URI可以通过
:meth:`Gtk.LinkButton.set_uri` 来设置，可以通过 :meth:`Gtk.LinkButton.get_uri` 来获取绑定的URI。


LinkButton 对象
^^^^^^^^^^^^^^^^^^

.. class:: Gtk.LinkButton(uri [, label])

    *uri* 是需要加载的网页的地址。label是显示的文本。如果label为 ``None`` 或者忽略，则显示网址。

    .. method:: get_uri()

    获取 :meth:`set_uri` 设置的URI。

    .. method:: set_uri(uri)

    设置按钮指向的 *uri* 地址。作为副作用，会取消按钮的 'visited' 状态。

Example
^^^^^^^

.. image:: images/linkbutton_example.png

.. literalinclude:: examples/linkbutton_example.py
    :linenos:

SpinButton
----------
:class:`Gtk.SpinButton` 是一种让用户设置某些属性的值的完美方法。
:class:`Gtk.SpinButton` 不是让用户直接在 :class:`Gtk.Entry` 中输入一个数字，
而是提供两个箭头让用户增加或减小显示的值。值也可以直接输入，可以附加检查以保证
输入的值在要求的范围内。 :class:`Gtk.SpinButton` 的主要属性通过
:class:`Gtk.Adjustment` 来设置。

要改变 :class:`Gtk.SpinButton` 显示的值，使用 :meth:`Gtk.SpinButton.set_value` 。
通过:meth:`Gtk.SpinButton.get_value` 或者 :meth:`Gtk.SpinButton.get_value_as_int` 获取按钮的值——
根据你的要求可以是整数或浮点值。

当spin button显示浮点数时，你可以通过
:meth:`Gtk.SpinButton.set_digits` 调整显示的浮点数的位数。

默认情况下， :class:`Gtk.SpinButton` 接受文本数据。如果你想限制其为数值，可以调用
:meth:`Gtk.SpinButton.set_numeric` ，并传递 ``True`` 。

我们也可以设置 :class:`Gtk.SpinButton` 显示的更新策略。有两种可选:
默认是即使输入的数据不合法也会显示；
我们也可以设置为只有输入的值正确时才需要更新——通过调用
:meth:`Gtk.SpinButton.set_update_policy` 。

SpinButton 对象
^^^^^^^^^^^^^^^^^^

.. class:: Gtk.SpinButton()

    .. method:: set_adjustment(adjustment)

        替换与该spin button关联的 :class:`Gtk.Adjustment` 。

    .. method:: set_digits(digits)

        设置spin button显示的精度——最高可以支持20个数字。

    .. method:: set_increments(step, page)

        设置按钮值增加的 step 和 page 。这会影响当按钮的箭头按下时值的变化速度。
        step是按下上下键改变的值大小，page则是指按下page up/down是改变的值大小。

    .. method:: set_value(value)

        设置按钮的值。

    .. method:: get_value()

        返回按钮的值——浮点数类型。

    .. method:: get_value_as_int()

        获取按钮的值——整型。

    .. method:: set_numeric(numeric)

        如果 *numeric* 为 ``False`` ，非数字的文本可以输入给spin button，否则只允许输入数值。

    .. method:: set_update_policy(policy)

        设置按钮的更新行为。这决定了按钮的值是总会更新还是只有值合法时才会更新。
        *policy* 参数的值可以是 :attr:`Gtk.SpinButtonUpdatePolicy.ALWAYS` 或者
        :attr:`Gtk.SpinButtonUpdatePolicy.IF_VALID` 。

Adjustment 对象
^^^^^^^^^^^^^^^^^^

.. class:: Gtk.Adjustment(value, lower, upper, step_increment, page_increment, page_size)

    :class:`Gtk.Adjustment` 对象代表一个有最大与最小界限的值，也包含每次增加的
    step和pagement。这在一些Gtk+窗口控件中使用，包括 :class:`Gtk.SpinButton` ，
    :class:`Gtk.Viewport` 和 :class:`Gtk.Range` 。

    *value* 为初始值， *lower* 为最小值， *upper* 为最大值，
    *step_increment* 为每次up/down键增加/减小的值， *page_increment* 是
    按下page up/down键改变的值大小，而 *page_size* 代表页大小。

Example
^^^^^^^

.. image:: images/spinbutton_example.png

.. literalinclude:: examples/spinbutton_example.py
    :linenos:
