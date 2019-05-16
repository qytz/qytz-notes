组合框（ComboBox）
===================
:class:`Gtk.ComboBox` 允许你从一个下拉列表中选择项目。
由于其占用更少的空间，应该是在屏幕上显示很多radio按钮的优选方案。如果恰当，他可以
显示很多条目额外的信息，如文本，图片，checkbox或者一个进度条。

:class:`Gtk.ComboBox` 与 :class:`Gtk.TreeView` 非常类似，他们都使用模型-视图模式；
有效选项的列表在tree model中指定，而选项的显示可以通过
:ref:`cell renderers <cellrenderers>` 适配到模型中。如果组合框包含很多的项目，
那么将他们显示在网格中比显示在列表中更好，调用
:meth:`Gtk.ComboBox.set_wrap_width` 可以实现。

:class:`Gtk.ComboBox` 控件通常会限制用户可能的选择，但是你可以设置一个
:class:`Gtk.Entry` ，允许用户输入任意的文本如果列表中的项目均不合适。
要设置 :class:`Gtk.Entry` ，使用静态方法
:meth:`Gtk.ComboBox.new_with_entry` 或者 :meth:`Gtk.ComboBox.new_with_model_and_entry`
来创建 :class:`Gtk.ComboBox` 的实例。

对于简单的文本选择下拉列表， :class:`Gtk.ComboBox` 的
模型-视图API可能有点大材小用（太复杂），因此
:class:`Gtk.ComboBoxText` 提供了一种更简单的选择。
:class:`Gtk.ComboBox` 和 :class:`Gtk.ComboBoxText` 均可以包含一个输入框。

ComboBox objects
----------------

.. class:: Gtk.ComboBox

    .. staticmethod:: new_with_entry()

        创建一个带有输入框的空的 :class:`Gtk.ComboBox` 。

    .. staticmethod:: new_with_model(model)

        创建一个新的 :class:`Gtk.ComboBox` ,模型被初始化为 *model* 。

    .. staticmethod:: new_with_model_and_entry(model)

        创建一个新的带有输入框的 :class:`Gtk.ComboBox` ，并且模型被初始化为 *model* 。

    .. method:: get_active_iter()

        返回一个 :class:`Gtk.TreeIter` 的实例，并且指向当前激活的项目。
        如果没有激活的项目，则返回 ``None`` 。

    .. method:: set_model(model)

        设置组合框使用的 *model* 。这会替换之前设置过的 model（如果有）。
        如果model为 ``None`` ，则会取消之前的设置。注意此方法不会清除单元格渲染器的内容。

    .. method:: get_model()

        返回作为组合框数据源的 :class:`Gtk.TreeModel` 。

    .. method:: set_entry_text_column(text_column)

        设置组合框要从模型的哪一列 *text_column* 来获取文笔内容，模型中的
        *text_column* 必须为 ``str`` 类型。

        只用组合框的 "has-entry" 属性为 ``True`` 时才可以用。

    .. method:: set_wrap_width(width)

        设置组合框的wrap width为 *width* 。wrap width指当你想弹出一个网格显示的
        列表时的首选列数。

ComboBoxText objects
--------------------

.. class:: Gtk.ComboBoxText

    .. staticmethod:: new_with_entry()

        创建一个空的带有输入框的 :class:`Gtk.ComboBoxText` 。

    .. method:: append_text(text)

        添加 *text* 到组合框的字符串列表中。

    .. method:: get_active_text()

        返回组合框当前激活的文本字符串，如果没有被选中的，则返回 ``None`` 。
        本函数会返回字符串的内容（不一定是列表中的项目）。

Example
-------

.. image:: images/combobox_example.png

.. literalinclude:: examples/combobox_example.py
    :linenos:
