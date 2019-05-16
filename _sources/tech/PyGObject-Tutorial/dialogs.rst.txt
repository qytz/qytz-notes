对话框（Dialog）
=================

对话框窗口与标准的窗口非常相似，用来向用户显示信息或者从用户那里获取信息，例如
通常用于提供一个首选项窗口。对话框主要的不同是一些预打包好的控件自动布局在窗口中。
我们可以简单地添加标签label、按钮、复选按钮等等，另一个很大的不同是响应的处理，
控制应用在用户与对话框的交互之后如何处理。

有很多你可能会觉得很有用的派生的对话框。 :class:`Gtk.MessageDialog` 用于绝大多数
的提示信息。但是其他的时候你肯呢个需要派生你自己的对话框类来提供更加复杂的功能。

自定义对话框
--------------

要打包控件到一个自定义的对话框，你应该把他们打包到一个 :class:`Gtk.Box` 中，可以
通过 :meth:`Gtk.Dialog.get_content_area` 获取box。要简单的添加一个按钮到对话框的
底部，你可以使用 :meth:`Gtk.Dialog.add_button` 。

可以通过 :class:`Gtk.Dialog.set_modal` 或者在 :class:`Gtk.Dialog` 的构造函数的
``flag`` 参数上包含 :attr:`Gtk.DialogFlags.MODAL` 创建 '模态' 对话框
（即会冻结对应用其他部分的反应）。

点击按钮会触发一个 "response" 信号，如果你想要阻塞等待对话框返回后再执行你的
控制流程，你可以调用 :meth:`Gtk.Dialog.run` ，该方法返回一个整型，可能是
:class:`Gtk.ResponseType` ，也可能是你在 :class:`Gtk.Dialog` 的构造函数或
:meth:`Gtk.Dialog.add_button` 方法中自定义的返回值。

最后，有两种方法可以删除对话框， :meth:`Gtk.Widget.hide` 从视图中移除对话框，但是
该对话框仍然在内存中，这通常在后边仍然需要显示的对话框很有用，可以阻止对此构造。
:meth:`Gtk.Widget.destroy` 方法则会在你不需要对话框时从内存中删除它，注意如果在
销毁后如果需要再次访问该对话框你必须重新构造，否则对话框窗口是空的。

Dialog 对象
^^^^^^^^^^^^^^

.. class:: Gtk.Dialog([title[, parent[, flags[, buttons]]])

    创建一个新的 :class:`Gtk.Dialog` ，标题设置为 *title* 并将临时的父窗口设置为
    *parent* 。 *flags* 参数可以用来设置对话框为模态(:attr:`Gtk.DialogFlags.MODAL`)
    和/或 设置为与其父窗口一起销毁(:attr:`Gtk.DialogFlags.DESTROY_WITH_PARENT`) 。

    *buttons* 为可以提供一个按钮和响应的不同按钮的元组。详情参考 :meth:`add_button` 。

    所有参数都是可选的，也可以用作key-word关键字参数。

    .. method:: get_content_area()

        返回对话框的内容区域。

    .. method:: add_button(button_text, response_id)

        根据给定的文本添加一个按钮(或者是stock button，如果 *button_text* 为
        :ref:`stock item <stock-items>`)，并设置当点击按钮时会触发 "响应" 信号
        并传递 *response_id* ，按钮会被添加都对话框活动区域的最后。

        *response_id* 可以为任何正整数或者以下 :class:`Gtk.ResponseType` 预定义的值：

        * :attr:`Gtk.ResponseType.NONE`
        * :attr:`Gtk.ResponseType.REJECT`
        * :attr:`Gtk.ResponseType.ACCEPT`
        * :attr:`Gtk.ResponseType.DELETE_EVENT`
        * :attr:`Gtk.ResponseType.OK`
        * :attr:`Gtk.ResponseType.CANCEL`
        * :attr:`Gtk.ResponseType.CLOSE`
        * :attr:`Gtk.ResponseType.YES`
        * :attr:`Gtk.ResponseType.NO`
        * :attr:`Gtk.ResponseType.APPLY`
        * :attr:`Gtk.ResponseType.HELP`

        创建的按钮控件会被返回，但通常用不到。

    .. method:: add_buttons(button_text, response_id[, ...])

        添加多个按钮到对话框，使用传递的按钮数据参数。本方法与重复调用
        :meth:`add_button` 方法一样。按钮数据对——按钮文本(或者 :ref:`stock item <stock-items>` )
        和响应id是分别传递的，例如::

            dialog.add_buttons(Gtk.STOCK_OPEN, 42, "Close", Gtk.ResponseType.CLOSE)

    .. method:: set_modal(is_modal)

        设置对话框为模态或非模态。模态对话框用户与应用程序的其他窗口交互。

    .. method:: run()

        阻塞于一个递归的循环直到对话框或者触发 "response" 信号或者被销毁。如果
        对话框在调用 :meth:`run` 期间被销毁，则会返回 :attr:`Gtk.ResponseType.NONE` 。
        否则会返回对信号的回应的响应id。

Example
^^^^^^^
.. image:: images/dialog_example.png

.. literalinclude:: examples/dialog_example.py
    :linenos:

消息对话框
-------------

:class:`Gtk.MessageDialog` 是一个便利类，用于创建简单的，标准的消息对话框，带有
一个消息，一个图标，及用于用户响应的按钮。你可以在 :class:`Gtk.MessageDialog` 的
构造函数中指定消息和文本的类型，也可以指定标准的按钮。

有一些对话框需要更多的描述到底发生了什么，此时可以添加次要的文本信息。这时创建
消息对话框时指定的主要的文本信息会设置为更大并为粗体。次要的消息可以通过
:meth:`Gtk.MessageDialog.format_secondary_text` 指定。

MessageDialog 对象
^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.MessageDialog([parent[, flags[, message_type[, buttons, [message_format]]]])

    创建一个新的 :class:`Gtk.MessageDialog` ，将临时的父窗口设置为
    *parent* 。 *flags* 参数可以用来设置对话框为模态(:attr:`Gtk.DialogFlags.MODAL`)
    和/或 设置为与其父窗口一起销毁(:attr:`Gtk.DialogFlags.DESTROY_WITH_PARENT`) 。

    *message_type* 可以设置为以下之一：

    * :attr:`Gtk.MessageType.INFO`: 提示消息
    * :attr:`Gtk.MessageType.WARNING`: 非致命警告信息
    * :attr:`Gtk.MessageType.QUESTION`: 需要用户选择的问题消息
    * :attr:`Gtk.MessageType.ERROR`: 致命的错误
    * :attr:`Gtk.MessageType.OTHER`: 非以上的，不会获取图标

    也可以给消息对话框设置多种的按钮，来从用户获取不同的响应，可以使用以下值之一：

    * :attr:`Gtk.ButtonsType.NONE`: 没有按钮
    * :attr:`Gtk.ButtonsType.OK`: 确定按钮
    * :attr:`Gtk.ButtonsType.CLOSE`: 关闭按钮
    * :attr:`Gtk.ButtonsType.CANCEL`: 取消按钮
    * :attr:`Gtk.ButtonsType.YES_NO`: 是和否按钮
    * :attr:`Gtk.ButtonsType.OK_CANCEL`: 确定和取消按钮

    最后， *message_format* 是用户要看到的文本信息。

    所有参数都是可选的，也可以用作key-word关键字参数。

    .. method:: format_secondary_text(message_format)

        设置消息对话框的次要文本信息为 *message_format* 。

        注意设置次要文本会使主要的文本(:class:`Gtk.MessageDialog` 构造函数的
        *message_format* 参数)变为粗体，除非你提供了明确的标记。

Example
^^^^^^^

.. image:: images/messagedialog_example.png

.. literalinclude:: examples/messagedialog_example.py
    :linenos:

文件选择对话框
-----------------

:class:`Gtk.FileChooserDialog` 用于 "文件/打开" 或者 "文件/保存" 菜单项很合适。
对于文件选择对话框你可以使用所有 :class:`Gtk.FileChooser` 和 :class:`Gtk.Dialog` 的方法。

当创建 :class:`Gtk.FileChooserDialog` 时你需要定义对话框的目的：

    * 要选择一个用于打开的问，用于文件/打开命令，使用 :attr:`Gtk.FileChooserAction.OPEN`
    * 要第一次保存一个文件，用于文件/保存命令，使用 :attr:`Gtk.FileChooserAction.SAVE` ，
      并使用 :meth:`Gtk.FileChooser.set_current_name` 指定一个建议的名字例如 "Untitled"
    * 要保存一个文件为不同的名字，用于文件/另存为命令，使用
      :attr:`Gtk.FileChooserAction.SAVE` ，并且通过
      :meth:`Gtk.FileChooser.set_filename` 设置已存在的文件的名字。
    * 要选择一个文件夹而不是文件，使用 :attr:`Gtk.FileChooserAction.SELECT_FOLDER`.

:class:`Gtk.FileChooserDialog` 继承自 :class:`Gtk.Dialog` ，因此按钮也有响应id如
:attr:`Gtk.ResponseType.ACCEPT` 和 :attr:`Gtk.ResponseType.CANCEL` ，这些也都可以
在 :class:`Gtk.FileChooserDialog` 的构造函数中指定。与 :class:`Gtk.Dialog` 类似，
你可以使用自定义的响应id，文件选择对话框应该至少包含以下id的按钮之一：

    * :attr:`Gtk.ResponseType.ACCEPT`
    * :attr:`Gtk.ResponseType.OK`
    * :attr:`Gtk.ResponseType.YES`
    * :attr:`Gtk.ResponseType.APPLY`

当用户完成文件的选择，你的程序可以获取选择的文件的文件名(:meth:`Gtk.FileChooser.get_filename`)
或者URI(:meth:`Gtk.FileChooser.get_uri`) 。

默认 :class:`Gtk.FileChooser` 一次只允许选择一个文件，要使用多选可以调用
:meth:`Gtk.FileChooser.set_select_multiple` 。获取选择的文件的列表可以使用
:meth:`Gtk.FileChooser.get_filenames` 或者 :meth:`Gtk.FileChooser.get_uris` 。

:class:`Gtk.FileChooser` 也支持各种选项使得文件和目录更加的可配置和访问。

    * :meth:`Gtk.FileChooser.set_local_only`: 只有本地文件可以选择。
    * :meth:`Gtk.FileChooser.show_hidden`: 显示隐藏文件。
    * :meth:`Gtk.FileChooser.set_do_overwrite_confirmation`: 如果文件选择对话框
      被配置为 :attr:`Gtk.FileChooserAction.SAVE` 模式，当用户输入的文件名已存在
      时，会显示一个确认对话框。

另外，你可以通过创建 :class:`Gtk.FileFilter` 对象并调用 :meth:`Gtk.FileChooser.add_filter`
来指定显示那些类型的文件。用户可以在文件选择对话框的底部的组合框选择添加的过滤器。
of the file chooser.

FileChooser 对象
^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.FileChooserDialog([title[, parent[, action[, buttons]]])

    创建一个新的 :class:`Gtk.FileChooserDialog` 并设置标题为 *title* ，临时的父窗口
    为 *parent* 。

    *action* 可以为一下之一：

    * :attr:`Gtk.FileChooserAction.OPEN`: 只允许用回选择一个已经存在的文件。
    * :attr:`Gtk.FileChooserAction.SAVE`: 允许用户使用一个已经存在的文件的名字或者输入一个新的文件名。
    * :attr:`Gtk.FileChooserAction.SELECT_FOLDER`: 允许用户选择一个已经存在的目录。
    * :attr:`Gtk.FileChooserAction.CREATE_FOLDER`: 允许用户命名一个新的或已经存在的目录。

    *buttons* 参数与 :class:`Gtk.Dialog` 的格式一样。

.. class:: Gtk.FileChooser

    .. method:: set_current_name(name)

        设置文件选择框当前文件的名字，就像用户输入的一样。

    .. method:: set_filename(filename)

        设置 *filename* 为文件选择框当前的文件名，改变到文件的父目录并选择列表中的
        文件，其他的文件都不会被选择。
        如果选择器为 :attr:`Gtk.FileChooserAction.SAVE` 模式，文件的基本名页会显示
        在对话框文件名输入框。

        注意文件必须存在，否则除了改变目录其他什么也不做。

    .. method:: set_select_multiple(select_multiple)

        设置可以选择多个文件，只在
        :attr:`Gtk.FileChooserAction.OPEN` 模式或
        :attr:`Gtk.FileChooserAction.SELECT_FOLDER` 有效。

    .. method:: set_local_only(local_only)

        设置是否只可以选择本地文件。

    .. method:: set_show_hidden(show_hidden)

        设置是否显示隐藏的文件和目录。

    .. method:: set_do_overwrite_confirmation(do_overwrite_confirmation)

        设置在保存模式是否提示覆盖。

    .. method:: get_filename()

        返回文件选择框当前选中的文件的名字。如果选中了多个文件，请使用
        :meth:`get_filenames` 代替。

    .. method:: get_filenames()

        返回在当前文件夹选中的文件和子目录的列表。返回的名字是绝对路径，如果当前
        目录的文件不是本地文件则会被忽略，要获取请使用 :meth:`get_uris` 来代替。

    .. method:: get_uri()

        返回文件选择框当前选中的文件的URI。如果多个文件被选中，请使用 :meth:`get_uris` 代替。

    .. method:: get_uris()

        返回当前目录选中的所有文件和子目录的列表，返回的名字是完整的URI。

    .. method:: add_filter(filter)

        添加 :class:`Gtk.FileFilter` 的实例 *filter* 到用户可以选择的过滤器列表。
        当过滤器被选中时只有通过过滤器的文件才会被显示。

.. class:: Gtk.FileFilter

    .. method:: set_name(name)

        设置过滤器的易于阅读的名字。这也是将会在文件选择框中显示的字符串。

    .. method:: add_mime_type(mime_type)

        添加一个允许给定的MIME类型的规则到过滤器。

    .. method:: add_pattern(pattern)

        添加一个允许shell风格的全局的规则到过滤器。

Example
^^^^^^^

.. image:: images/filechooserdialog_example.png

.. literalinclude:: examples/filechooserdialog_example.py
    :linenos:
