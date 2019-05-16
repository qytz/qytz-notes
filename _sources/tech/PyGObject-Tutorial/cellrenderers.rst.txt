.. _cellrenderers:

单元格渲染器（CellRenderers）
===============================

:class:`Gtk.CellRenderer` 控件用来在例如 :class:`Gtk.TreeView` 或 :class:`Gtk.ComboBox`
这样的控件中显示信息。这些单元格渲染器与相关联的控件联系紧密并且非常强大，有大量的配置选项用来以
不同的方式来显示大量的数据。有七种 :class:`Gtk.CellRenderer` 可以用于不同的目的。:

    * :class:`Gtk.CellRendererText`
    * :class:`Gtk.CellRendererToggle`
    * :class:`Gtk.CellRendererPixbuf`
    * :class:`Gtk.CellRendererCombo`
    * :class:`Gtk.CellRendererProgress`
    * :class:`Gtk.CellRendererSpinner`
    * :class:`Gtk.CellRendererSpin`
    * :class:`Gtk.CellRendererAccel`

CellRendererText
----------------

:class:`Gtk.CellRendererText` 在单元格中渲染给定的文本，并使用其属性提供的字体、颜色与style信息。
如果 "ellipsize" 允许，文本太长时会显示为带省略号的形式。

默认 :class:`Gtk.CellRendererText` 控件中的文本是不可编辑的。可以通过其 "editable" 属性设置为
``True`` 来改变该行为。

.. code-block:: python

    cell.set_property("editable", True)

可编辑之后你就可以连接 "editable" 信号来更新你的 :class:`Gtk.TreeModel` 了。

CellRendererText 对象
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererText()

    创建一个新的 :class:`Gtk.CellRendererText` 的实例。使用对象属性来调整文本的绘制。
    与 :class:`Gtk.TreeViewColumn` 一起，你可以绑定 :class:`Gtk.TreeModel` 的值到一个属性。
    例如，你可以绑定 "text" 属性与模型中的一个字符串值，来在 :class:`Gtk.TreeView` 的每一行渲染不同的文本。

例子
^^^^^^^

.. image:: images/cellrenderertext_example.png

.. literalinclude:: examples/cellrenderertext_example.py
    :linenos:

CellRendererToggle
------------------

:class:`Gtk.CellRendererToggle` 在单元格内渲染一个 toggle button 。
按钮被渲染为一个radio 按钮或者checkbutton按钮，根据 "radio" 属性。当激活（active）后会
激发 "toggled" 信号。

由于 :class:`Gtk.CellRendererToggle` 有两个状态，active 和 not active，你要将
"active" 属性与一个布尔值的模型绑定，这样才能使得check button的状态反映出模型的状态。

CellRendererToggle 对象
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererToggle

    创建一个新的 :class:`Gtk.CellRendererToggle` 实例。

    .. method:: set_active(setting)

        设置单元格渲染器的是Activates 还是 deactivates 。

    .. method:: get_active()

        返回单元格渲染器的active状态。

    .. method:: set_radio(radio)

        如果 *radio* 为 ``True``，单元格渲染器会渲染一个radio样式的toggle按钮（即
        一个互斥的按钮组），如果为 ``False`` ，则渲染为一个一个 check toggle。

    .. method:: get_radio()

        返回是否被渲染为一个radio 按钮组。

Example
^^^^^^^

.. image:: images/cellrenderertoggle_example.png

.. literalinclude:: examples/cellrenderertoggle_example.py
    :linenos:

CellRendererPixbuf
------------------

:class:`Gtk.CellRendererPixbuf` 用于在单元格中渲染一张图片。
允许渲染一个给定的 :class:`Gdk.Pixbuf` (设置 "pixbuf" 属性) 或者
:ref:`stock item <stock-items>` (设置 "stock-id" 属性)。

CellRendererPixbuf 对象
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererPixbuf

    创建一个新的 :class:`Gtk.CellRendererPixbuf` 。使用对象属性来调整渲染的
    参数，例如你可以绑定单元格渲染器的 "pixbuf" 或者 "stock-id"
    属性到模型的pixbuf值，这样就可以在 :class:`Gtk.TreeView` 的每一行渲染不同的图片。

Example
^^^^^^^

.. image:: images/cellrendererpixbuf_example.png

.. literalinclude:: examples/cellrendererpixbuf_example.py
    :linenos:

CellRendererCombo
-----------------

:class:`Gtk.CellRendererCombo` 像
:class:`Gtk.CellRendererText` 一样在单元格内渲染文本，但是后者只提供了一个
简单的输入框来编辑文本，而 :class:`Gtk.CellRendererCombo` 提供了一个
:class:`Gtk.ComboBox` 控件来编辑文本。在组合框（combo box）中显示的
值通过 "model" 属性从 :class:`Gtk.TreeModel` 中获取。

组合框单元格渲染器对于添加文本到组合框列表中很严格，通过设置 "text-column" 属性
来设置要显示的列。

:class:`Gtk.CellRendererCombo` 有两种操作模式，即有或者没有关联的
:class:`Gtk.Entry` 控件，依赖于 "has-entry" 属性的值。

CellRendererCombo 对象
^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererCombo

    创建一个新的 :class:`Gtk.CellRendererCombo` 。使用对象的属性来调整渲染效果。
    例如绑定单元格渲染器的 "text" 属性到模型的string字段来在
    :class:`Gtk.TreeView` 的每一行显示不同的文本。

Example
^^^^^^^

.. image:: images/cellrenderercombo_example.png

.. literalinclude:: examples/cellrenderercombo_example.py
    :linenos:

CellRendererProgress
--------------------

:class:`Gtk.CellRendererProgress` 渲染一个数值为一个显示在单元格中的进度条。
你也可以在进度条上面显示文本。

进度条的进度百分比值可以通过改变 "value" 属性来修改。类似于
:class:`Gtk.ProgressBar` ，你可以通过设置 "pulse" 属性而不是 "value"
属性来使能 *activity mode* 。

CellRendererProgress 对象
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererProgress

    创建一个新的 :class:`Gtk.CellRendererProgress`.

Example
^^^^^^^

.. image:: images/cellrendererprogress_example.png

.. literalinclude:: examples/cellrendererprogress_example.py
    :linenos:

CellRendererSpin
----------------

:class:`Gtk.CellRendererSpin` 与renders text in a cell like
:class:`Gtk.CellRendererText` 类似，在单元格中渲染文本，但与后者提供一个简单的
输入框编辑不同， :class:`Gtk.CellRendererSpin` 提供了一个
:class:`Gtk.SpinButton` 控件。当然这意味着文本必须是一个float浮点数。

spinbutton 的范围从 "adjustment" 属性来获取，可以设置映射为模型的一列。
:class:`Gtk.CellRendererSpin` 也可以通过属性来设置步进值及显示的数字的位数。

CellRendererSpin 对象
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.CellRendererSpin

    创建一个新的 :class:`Gtk.CellRendererSpin` 。

Example
^^^^^^^

.. image:: images/cellrendererspin_example.png

.. literalinclude:: examples/cellrendererspin_example.py
    :linenos:
