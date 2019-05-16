拖拽支持
=============
.. note::
    低于3.0.3版本的PyGObject有一个bug使得拖拽功能不正确，因此下面的例子要求
    PyGObject 的版本大于等于3.0.3。

要在控件间设置拖拽功能，首先要使用 :meth:`Gtk.Widget.drag_source_set` 选择一个
拖拽的源控件，然后通过 :meth:`Gtk.Widget.drag_dest_set` 设置拖拽的目的控件，然后
在两个控件上处理相关的信号。

有一些专门的控件并不使用 :meth:`Gtk.Widget.drag_source_set` 和
:meth:`Gtk.Widget.drag_dest_set` ，而是使用一些特殊的函数
(例如 :class:`Gtk.TreeView` 和 :class:`Gtk.IconView`)。

一个基本的拖拽支持只要求源控件连接 "drag-data-get" 信号，目地控件连接
"drag-data-received" 信号。更多复杂的功能如指定释放的区域和定制拖拽的图片则要求
连接 :ref:`额外的信号 <drag-signals>` 并和其提供的 :class:`Gdk.DragContext` 对象交互。

要在源和目的控件间传递数据，你必须使用 :class:`Gtk.SelectionData` 的get与set函数
与 :ref:`"drag-data-get" <drag-signals>` 和 :ref:`"drag-data-received" <drag-signals>`
信号提供的 :class:`Gtk.SelectionData` 变量交互。

Target Entries
--------------
要知道拖拽的源和目的发送和接收的数据，需要一个 :class:`Gtk.TargetEntry's <Gtk.TargetEntry>`
的列表。 :class:`Gtk.TargetEntry` 描述了被拖拽源发送或被拖拽目的接收的一片数据。

有两种方式添加 :class:`Gtk.TargetEntry's <Gtk.TargetEntry>` 源或目的。如果是简单的
拖拽支持并且源目的节点都是不同的类型，可以使用函数组
:meth:`mentioned here <Gtk.widget.grag_source_add_text_targets>` 。如果需要拖拽多种
类型的数据并对数据做更加复杂的操作，则需要使用 :meth:`Gtk.TargetEntry.new` 创建
:class:`Gtk.TargetEntry的 <Gtk.TargetEntry的>` 。

拖拽方法与对象
---------------------------------
.. class:: Gtk.Widget

    .. method:: drag_source_set(start_button_mask, targets, actions)

    设置控件为拖拽源。

    *start_button_mask* 是多个:attr:`Gdk.ModifierType` 的组合设置了要使拖拽支持
    发生要按下的按钮。 *targets* 是一个 :class:`Gtk.TargetEntry` 的列表描述了要
    在源和目的之间传递的数据。 *actions* 是 :attr:`Gdk.DragAction` 的组合标记了
    可能的拖拽动作。

    .. method:: drag_dest_set(flags, targets, actions)

    设置控件为拖拽的目的。

    *flags* 为 :attr:`Gtk.DestDefaults` 的组合配置了拖拽发生时的动作。
    *targets* 是 :class:`Gtk.TargetEntry的 <Gtk.TargetEntry>` 的列表描述了拖拽
    源与目的之间的数据。
    *actions* 是 :attr:`Gdk.DragAction` 的组合描述了可能的拖拽动作。

    .. method:: drag_source_add_text_targets()
                drag_dest_add_text_targets()

    添加 :class:`Gtk.TargetEntry` 为拖拽源或目的，其包含了一段文本。

    .. method:: drag_source_add_image_targets()
                drag_dest_add_image_targets()

    添加 :class:`Gtk.TargetEntry` 为拖拽源或目的，其包含了:class:`GdkPixbuf.Pixbuf` 。

    .. method:: drag_source_add_uri_targets()
                drag_dest_add_uri_targets()

    添加 :class:`Gtk.TargetEntry` 为拖拽源或目的，其包含了一个 URI 列表。

.. class:: Gtk.TargetEntry

    .. staticmethod:: new(target, flags, info)

    创建一个新的目的节点。

    *target* 为一个字符串描述了目的节点描述的数据的类型。

    *flags* 控制数据在拖拽源/目的之间传递的条件，为 :attr:`Gtk.TargetFlags` 的组合：

    * :attr:`Gtk.TargetFlags.SAME_APP` - 只在相同程序间传递。
    * :attr:`Gtk.TargetFlags.SAME_WIDGET` - 只在相同控件间传递。
    * :attr:`Gtk.TargetFlags.OTHER_APP` - 只在不同程序间传递。
    * :attr:`Gtk.TargetFlags.OTHER_WIDGET` - 只在不同控件间传递。

    *info* 为应用程序ID，可以用来决定在一次拖拽操作中不同的数据片。

.. class:: Gtk.SelectionData

    .. method:: get_text()

    返回selection data中包含的文本数据。

    .. method:: set_text(text)

    设置selection data包含的文本为 *text* 。

    .. method:: get_pixbuf()

    返回selection data包含的pixbuf图像。

    .. method:: set_pixbuf(pixbuf)

    设置selection data包含的pixbuf为 *pixbuf* 。

.. _drag-signals:

拖拽源信号
-------------------
+--------------------+----------------------------------------------+-----------------------------------+
| 名字               | 触发时机                                     | 通常目的                          |
+====================+==============================================+===================================+
| drag-data-get      | 拖拽目地请求数据时                           | 在拖拽源与目的间传递数据          |
+--------------------+----------------------------------------------+-----------------------------------+
| drag-data-delete   | action为 Gdk.DragAction.MOVE 的拖拽操作完成  | 完成 'move' 操作时删除源数据      |
+--------------------+----------------------------------------------+-----------------------------------+
| drag-data-end      | 拖拽完成                                     | 撤销任何拖拽开始后的动作          |
+--------------------+----------------------------------------------+-----------------------------------+

Drag Destination Signals
------------------------
+--------------------+----------------------------------------------------------+
| 名字               | 触发时机                | 通常目的                       |
+====================+=========================+================================+
| drag-motion        | 拖拽图标移动到目地区域  | 只允许拖拽到指定的区域         |
+--------------------+-------------------------+--------------------------------+
| drag-drop          | 在目地区域释放了图标    | 只允许在指定的区域释放数据     |
+--------------------+-------------------------+--------------------------------+
| drag-data-received | 拖拽目地收到了数据      | 在源与目地之间传递数据         |
+--------------------+-------------------------+--------------------------------+

Example
-------

.. image:: images/drag_and_drop_example.png
.. literalinclude:: examples/drag_and_drop_example.py
    :linenos:
