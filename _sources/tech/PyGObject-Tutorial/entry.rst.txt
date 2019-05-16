Entry输入框
===========

输入框控件允许用户输入文本，你可以使用
:meth:`Gtk.Entry.set_text` 方法来改变输入框的内容。使用
:meth:`Gtk.Entry.get_text` 来获取输入框当前的内容。你也可以使用
:meth:`Gtk.Entry.set_max_length` 限制输入框可以输入的最大文本数。

有时候你想要设置输入框只读，可以通过传递 ``False`` 给方法 :meth:`Gtk.Entry.set_editable` 。

输入框也可以用来从用户获取密码，通常要隐藏用户的输入以避免输入被地丧恶人看见，调用
:meth:`Gtk.Entry.set_visibility` 传递 ``False`` 可以使输入的文本被隐藏。

:class:`Gtk.Entry` 也可以在文本的后面显示进度或者活动的信息，类似于
:class:`Gtk.ProgressBar` 控件，用在浏览器中显示下载的进度。要使输入框显示这样的信息，需要调用
:meth:`Gtk.Entry.set_progress_fraction` , :meth:`Gtk.Entry.set_progress_pulse_step` 或
:meth:`Gtk.Entry.progress_pulse` 。

另外，输入框也可以在前面或者后面显示图标，这些图标可以通过点击激活，可以设置为拖拽源，
也可以提示信息。要添加这样的图标，可以调用 :meth:`Gtk.Entry.set_icon_from_stock` 或者任何一个
从图标的名字、pixbuf或icon主题中设置图标的变种函数。要设置图标的提示信息，使用
:meth:`Gtk.Entry.set_icon_tooltip_text` 或者相应的函数。

Entry 输入框对象
-----------------

.. class:: Gtk.Entry()

    .. method:: get_text()

        获取输入框控件的内容。

    .. method:: set_text(text)

        设置控件的文本，会替换原来的内容。

    .. method:: set_visibility(visible)

        设置输入框的内容是否可见。当 *visible* 为 ``False`` 时，
        字符显示为不可见的字符——即使是从其他地方复制过来的。

    .. method:: set_max_length(max)

        设置允许输入文本的最大长度。如果当前的内容比设置的长度常，则文本会被截断。

    .. method:: set_editable(is_editable)

        设置用户可否比啊及输入框中的内容。如果 *is_editable* 为 ``True`` ，用户可以编辑文本。

    .. method:: set_progress_fraction(fraction)

        设置进度条指针填充到的进度，设置的值必须介于0.0和1.0之间，包括0和1。

    .. method:: set_progress_pulse_step(fraction)

        设置每次调用 :meth:`progress_pulse` 时进度反弹块移动的宽度占输入框总宽度的百分比。

    .. method:: progress_pulse()

        一些进度向前走了，但是你不知道前进了多少，调用词函数使输入框的进度指示针进入活动状态，
        这样会有一个反弹块前后移动。每次调用 :meth:`progress_pulse` 会使反弹块移动一点
        （移动的多少由 :meth:`set_progress_pulse_step` 来决定）。

    .. method:: set_icon_from_stock(icon_pos, stock_id)

        设置在输入框的特定位置显示图标，图标 *stock_id* 参考 :ref:`stock item <stock-items>` 。
        如果 *stock_id* 为 ``None`` ，则不会显示图标。

        *icon_pos* 指定了图标放在输入框的哪一侧，可能的值有：

        * :attr:`Gtk.EntryIconPosition.PRIMARY`:
          在输入框的开始（要根据文本的方向）。
        * :attr:`Gtk.EntryIconPosition.SECONDARY`:
          在输入框的结尾（要根据文本的方向）。

    .. method:: set_icon_tooltip_text(icon_pos, tooltip)

        设置 *tooltip* 的内容作为指定位置的图标的提示信息。如果 *tooltip* 为 ``None`` ，
        那么之前设置的提示信息被移除。

        *icon_pos* 允许的值参见 :meth:`set_icon_from_stock` 。

Example
-------

.. image:: images/entry_example.png

.. literalinclude:: examples/entry_example.py
    :linenos:
