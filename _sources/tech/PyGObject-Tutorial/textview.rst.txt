Multiline Text Editor
=====================

:class:`Gtk.TextView` 控件可以用来显示和编辑大量的格式化的文本。与 :class:`Gtk.TreeView`
类似，其也有一个模型/视图的设计， :class:`Gtk.TextBuffer` 就是代表正在被编辑的文本
的模型。模型也允许两个或更多个的 :class:`Gtk.TextView` 共享同一个 :class:`Gtk.TextBuffer` ，
并允许这些文本有不同的显示。或者你也可以在同一个 :class:`Gtk.TextView` 的不同时间显示
不同 text buffer 的文本。

视图（The View）
------------------

:class:`Gtk.TextView` 就是用户可以添加、编辑或者删除文本的前端，其通常用来编辑
多行的文本。当创建一个 :class:`Gtk.TextView` 时其自动包含一个默认的 :class:`Gtk.TextBuffer` ，
你可以通过 :meth:`Gtk.TextView.get_buffer` 来获取。

默认情况下，文本可以在 :class:`Gtk.TextView` 中被添加、编辑与删除，你可以通过调用
:meth:`Gtk.TextView.set_editable` 来禁止编辑。如果文本不可被编辑，你也通常想要使用
:meth:`Gtk.TextView.set_cursor_visible` 来隐藏文本光标。在有些时候可以通过
:meth:`Gtk.TextView.set_justification` 来设置文本的对齐方式很有用，文本可以显示为
左对齐(:attr:`Gtk.Justification.LEFT`)，右对齐(attr:`Gtk.Justification.RIGHT`)，或者
中间对齐(attr:`Gtk.Justification.CENTER`)，或者占满整行(attr:`Gtk.Justification.FILL`)。

:class:`Gtk.TextView` 的另一项默认设置是长行会一直水平延伸知道遇到一个断行。调用
:meth:`Gtk.TextView.set_wrap_mode` 可以使文本自动换行一避免文本跑出屏幕边缘。

TextView 对象
^^^^^^^^^^^^^^^^

.. class:: Gtk.TextView

    创建一个新的 :class:`Gtk.TextView` 并关联一个空的 :class:`Gtk.TextBuffer` 。

    .. method:: get_buffer()

        返回 text view 正在显示的 :class:`Gtk.TextBuffer` 。

    .. method:: set_editable(editable)

        设置 :class:`Gtk.TextView` 的文本是否可编辑。

    .. method:: set_cursor_visible(visible)

        设置现在光标的位置是否显示。不可编辑文本不应该有一个可见的光标，因此你
        可能会关闭光标的显示。

    .. method:: set_justification(justification)

        设置文本的额默认对齐方式。

        *justification* 的值可以是下列之一：

        * :attr:`Gtk.Justification.LEFT`: 文本左对齐。
        * :attr:`Gtk.Justification.RIGHT`: 文本右对齐。
        * :attr:`Gtk.Justification.CENTER`: 文本居中对齐。
        * :attr:`Gtk.Justification.FILL`: 文本占满整行。

    .. method:: set_wrap_mode(wrap_mode)

        设置view是否自动断行。

        *wrap_mode* 的值可以是下列之一：

        * :attr:`Gtk.WrapMode.NONE`: 不自动断行，文本域会一直随着文本变宽。
        * :attr:`Gtk.WrapMode.CHAR`: 自动断行，可以光标可以出现的地方断行（通常字符之间）。
        * :attr:`Gtk.WrapMode.WORD`: 自动断行，可以在单词之间断行。
        * :attr:`Gtk.WrapMode.WORD_CHAR`: 自动断行，可以在单词之间断行，但如果
          空间不够时Wrap text, 也可以在 `graphemes`_ 出断行。

模型（The Model）
---------------------

:class:`Gtk.TextBuffer` 是 :class:`Gtk.TextView` 控件的核心，用来保存
:class:`Gtk.TextView` 显示的文本。设置和获取文本内容可以他用过
:meth:`Gtk.TextBuffer.set_text` 和 :class:`Gtk.TextBuffer.get_text` 。
但是绝大多数的文本操作是通过 *iterators* 来完成的，即 :class:`Gtk.TextIter` 。
iterator迭代器代表了文本buffer中两个字符之间的一个位置。迭代器并不是一直有效的，
一旦文本内容被修改并影响了buffer的内容，所有的迭代去就都无效了。

正因为此，迭代器不能用来在buffer修改前后保留位置。要保存一个位置，使用 :class:`Gtk.TextMark` 。
一个text buffer包含两个内建的标记，"insert" 标记光标的位置，"selection_bound" 标记，
可以通过 :meth:`Gtk.TextBuffer.get_insert` 和 :meth:`Gtk.TextBuffer.get_selection_bound`
来获得他们。默认 :class:`Gtk.TextMark` 的位置是不显示的，可以通过
:meth:`Gtk.TextMark.set_visible` 设置。

有很多方法可以获取 :class:`Gtk.TextIter` 。例如， :meth:`Gtk.TextBuffer.get_start_iter`
返回只想text buffer地一个位置的迭代器，而 :meth:`Gtk.TextBuffer.get_end_iter` 则返回
最后一个有效字符处的迭代器。获取选中文本的边界可以通过 :meth:`Gtk.TextBuffer.get_selection_bounds` 。

要在一个指定位置插入文本请使用 :meth:`Gtk.TextBuffer.insert` 。另一个非常有用的方法
:meth:`Gtk.TextBuffer.insert_at_cursor` 可以在光标指向的位置插入文本。要删除一部分
文本请使用 :meth:`Gtk.TextBuffer.delete` 。

另外，:class:`Gtk.TextIter` 可以通过 :meth:`Gtk.TextIter.forward_search` 和
:meth:`Gtk.TextIter.backward_search` 用来搜索文本。根据需求可以使用buffer开始和结束
的iters来进行向前/后的搜索。

TextBuffer 对象
^^^^^^^^^^^^^^^^^^

.. class:: Gtk.TextBuffer

    .. method:: set_text(text[, length])

        删除buffer当前的内容，并插入 *length* 个 *text* 中的字符。
        如果 *length* 为-1或忽略， *text* 全部被插入。

    .. method:: get_text(start_iter, end_iter, include_hidden_chars)

        返回从 *start_iter* (包含)和 *end_iter* (不含)之间的文本，如果
        *include_hidden_chars* 为 ``False`` ，则不包含未显示的文本。

    .. method:: get_insert()

        返回代表当前光标位置(插入点)的 :class:`Gtk.TextMark` 。

    .. method:: get_selection_bound()

        返回代表选中区域边界的 :class:`Gtk.TextMark` 。

    .. method:: create_mark(mark_name, where[, left_gravity])

        在 :class:`Gtk.TextIter` *where* 处创建一个 :class:`Gtk.TextMark` 。
        如果 *mark_name* 为 ``None`` ，则mark是匿名的。如果一个标记有left_gravity，
        文本被插入到当前位置后，标记会移动到新插入文本的左边。如果标记为right_gravity
        (*left_gravity* 为 ``False``)，标记会移动到新插入文本的右边。因此标准的
        从左到右的光标为right gravity的标记（当你输入的时候，光标会出现在你输入文本的右边）。

        如果 *left_gravity* 被忽略，默认为 ``False`` 。

    .. method:: get_mark(mark_name)

        返回buffer中名字为mark_name的 :class`Gtk.TextMark` ，如果不存在则返回 ``None`` 。

    .. method:: get_start_iter()

        返回指向buffer地一个位置的 :class:`Gtk.TextIter` 。

    .. method:: get_end_iter()

        返回只想buffer最后一个有效字符的 :class:`Gtk.TextIter` 。

    .. method:: get_selection_bounds()

        返回包含两个 :class:`Gtk.TextIter` tuple对象，分别指向选中的第一个字符和
        后不第一个未选中的字符。如果没有文本被选中则返回空的tuple。

    .. method:: insert(text_iter, text[, length])

        在 *text_iter* 处插入 *text* 的 *length* 个字符。如果 *length* 为-1或忽略，
        全部的 *text* 会被插入。

    .. method:: insert_at_cursor(text[, length])

        :meth:`insert` 的简单调用，使用光标位置作为插入点。

    .. method:: delete(start_iter, end_iter)

        删除 *start_iter* 与 *end_iter* 之间的文本。

    .. method:: create_tag(tag_name, \*\*kwargs)

        创建一个tag并添加到buffer的tag表中。

        如果 *tag_name* 为 ``None`` ，则tag是匿名的，否则tag_name不能与tag表中
        已经存在的tag重名。

        *kwargs* 为任意数量的键值对，代表了tag的属性列表，可以通过 ``tag.set_property`` 来设置。

    .. method:: apply_tag(tag, start_iter, end_iter)

        应用 *tag* 到给定范围的文本。

    .. method:: remove_tag(tag, start_iter, end_iter)

        删除给定范围内所有的 *tag* 。

    .. method:: remove_all_tags(start_iter, end_iter)

        删除给定范围内所有的tag。


.. class:: Gtk.TextIter

    .. method:: forward_search(needle, flags, limit)

        向前搜索 *needle* 。搜索在达到limit后不会再继续。

        *flags* 可以为下列之一，或者他们的组合（通过或操作符 ``|`` ）。

        * 0: 精确匹配
        * :attr:`Gtk.TextSearchFlags.VISIBLE_ONLY`: 匹配可能在 *needle* 中间穿插
          有不可见字符，即 *needle* 为匹配到的字符串的可能不连续的子序列。
        * :attr:`Gtk.TextSearchFlags.TEXT_ONLY`: 匹配可能包含图像pixbuf或者子空间
          混合在匹配到的范围内。
        * :attr:`Gtk.TextSearchFlags.CASE_INSENSITIVE`: 匹配忽略大小写。

        返回包含指向开始与匹配到的文本后边的 :class:`Gtk.TextIter` 的元组。如果
        没有找到，则返回 ``None`` 。

    .. method:: backward_search(needle, flags, limit)

        与 :meth:`forward_search` 相同，但是向后搜索。


.. class:: Gtk.TextMark

    .. method:: set_visible(visible)

        设置标记的可见性。插入点通常是可见的，即你可以看到一个竖直的光标条；而且，
        text控件也会使用一个可见的标记来指示拖拽操作的释放点。绝大多数其他的比较
        是不可见的。标记默认是不可见的。

Tags
----

buffer内的文本可以通过tag来标记。tag就是一个可以应用到一个文本范围的属性。例如，
"bold" tag使应用到文本加粗。然而tag的概念比其更多，tag不一定会影响外观，也可能会
影响鼠标和按键的行为，"lock" 可以锁定一段文本使用户不能编辑，或者数不尽的其他的事情。
tag由 :class:`Gtk.TextTag` 对象代表。一个 :class:`Gtk.TextTag` 可以应用到任何数量
的文本范围，任何数量的buffer。

所有的tag都存储在 :class:`Gtk.TextTagTable` 中。一个tab表定义了一系列的tag并可以一起使用。
每一个buffer都有一个与之关联的tag表，只有表中的tag才可以应用到buffer。但一个tag表可以
在多个buffer间共享。

要指定buffer内的一部分为本应该有特定的格式，你必须先定义该格式的tag，然后使用
:meth:`Gtk.TextBuffer.create_tag` 和 :meth:`Gtk.TextBuffer.apply_tag` 来将tag应用到文本区域。 ::

    tag = textbuffer.create_tag("orange_bg", background="orange")
    textbuffer.apply_tag(tag, start_iter, end_iter)

以下列出一些应用到文本的通常使用的风格：

    * 背景颜色("foreground" property)
    * 前景颜色("background" property)

    * 下划线("underline" property)
    * 粗体("weight" property)
    * 斜提("style" property)
    * 删除线("strikethrough" property)
    * 对齐("justification" property)
    * 大小("size" and "size-points" properties)
    * 自动换行("wrap-mode" property)

你也可以使用 :meth:`Gtk.TextBuffer.remove_tag` 删除某个特定的tag，或者使用
:meth:`Gtk.TextBuffer.remove_all_tags` 删除给的区域所有的tag。

Example
-------

.. image:: images/textview_example.png

.. literalinclude:: examples/textview_example.py
    :linenos:


.. _graphemes: http://developer.gnome.org/pango/stable/pango-Text-Processing.html#pango-get-log-attrs
