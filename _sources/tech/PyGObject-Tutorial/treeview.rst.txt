树与列表控件
=====================

:class:`Gtk.TreeView` 及其相关的控件绝对是用来显示数据的一个及其强大的控件。
使用时通常与 :class:`Gtk.ListStore` 或 :class:`Gtk.TreeStore` 关联，以提供一种
显示数据的方法并提供了很多种维护数据的方法，包括：

    * 数据添加、删除或编辑后自动更新；
    * 鼠标拖拽支持；
    * 数据排序；
    * 支持嵌入check box、进度条等控件；
    * 可重新排序及调整宽度的列
    * 数据过滤

由 :class:`Gtk.TreeView` 的强大与灵活自然也就使其变的很复杂。由于需要的函数很多
对于初级开发者很难掌握其正确的使用。

The Model(模型)
----------------
每一个 :class:`Gtk.TreeView` 都有一个与之关联的 :class:`Gtk.TreeModel` ，
TreeMode包含要显示给TreeView的数据。而每一个 class:`Gtk.TreeModel` 可以被多个
:class:`Gtk.TreeView` 使用。例如这样可以允许同一份数据同时被以两种不同的方式显示
和编辑，或者是两个TreeView分别显示TreeNode数据不同的列，这类似于使用两条SQL 查询
（或者视图？）就可以从同一个数据库表里取出不同的字段。

尽管理论上你可以实现你自己的模型，但你通常都是使用
:class:`Gtk.ListStore` 或者 :class:`Gtk.TreeStore` 。
:class:`Gtk.ListStore` 包含很多行简单的数据，每一行并没有“子行”，而
:class:`Gtk.TreeStore` 则是包含很多行的数据，同时每一行都可以有其孩子行。

当你构造一个模型的时候，你要指定你的每列数据的类型。

.. code-block:: python

    store = Gtk.ListStore(str, str, float)

上面的代码创建了一个列表存储，包含三列，两列类型是字符串，一列是浮点数。

要向这个模型添加数据使用 :meth:`Gtk.ListStore.append` 或者
:meth:`Gtk.TreeStore.append` ——根据你创建的是那种类型的数据模型。

.. code-block:: python

    treeiter = store.append(["The Art of Computer Programming", "Donald E. Knuth", 25.46])

这两个方法都是返回一个 :class:`Gtk.TreeIter` 的实例，并指向最新插入的行。你可以
通过调用 :meth:`Gtk.TreeMode.get_iter` 来取回 :class:`Gtk.TreeIter` 。

一旦数据已经被插入你就可以通过tree的迭代器（tree iter）和列索引取回或者修改数据

.. code-block:: python

    print store[treeiter][2] # Prints value of third column
    store[treeiter][2] = 42.15

基于Python内建的 :class:`list` 对象，你可以使用 :func:`len` 获取行数并使用切片
操作获取或者他们的值。

.. code-block:: python

    # Print number of rows
    print len(store)
    # Print all but first column
    print store[treeiter][1:]
    # Print last column
    print store[treeiter][-1]
    # Set first two columns
    store[treeiter][:2] = ["Donald Ervin Knuth", 41.99]

迭代一个tree model所有行的方法也很简单。

.. code-block:: python

    for row in store:
        # Print values of all columns
        print row[:]

记住，如果你使用了 :class:`Gtk.TreeStore` ，上面的代码只会遍历顶层的行，
但是不会遍历节点的孩子。要遍历所有的行和他们的孩子，使用
``print_tree_store`` 代替。

.. code-block:: python

    def print_tree_store(store):
        rootiter = store.get_iter_first()
        print_rows(store, rootiter, "")

    def print_rows(store, treeiter, indent):
        while treeiter != None:
            print indent + str(store[treeiter][:])
            if store.iter_has_child(treeiter):
                childiter = store.iter_children(treeiter)
                print_rows(store, childiter, indent + "\t")
            treeiter = store.iter_next(treeiter)

除了像上面那样使用list-like方式访问 :class:`Gtk.TreeModel` 中的数据，你也可以使用
:class:`Gtk.TreeIter` 或者 :class:`Gtk.TreePath` 的实例，这两个君代表了一个tree model
的特定的一行数据。
你页可以通过调用 :meth:`Gtk.TreeModel.get_iter` 将path转换为迭代器（iter）。
鉴于 :class:`Gtk.ListStore` 只包含一层，即节点没有子节点，path实际上就是你要访问的
一行数据的index。

.. code-block:: python

    # Get path pointing to 6th row in list store
    path = Gtk.TreePath(5)
    treeiter = liststore.get_iter(path)
    # Get value at 2nd column
    value = liststore.get_value(treeiter, 1)

对于 :class:`Gtk.TreeStore` ，path其实就是索引或者字符串的list。字符串的形式是以冒号分割的数字，每一个数字代表那一层的偏移。
例如，path "0" 代表根节点，path "2:4" 代表第三个节点的第五个孩子。

.. code-block:: python

    # Get path pointing to 5th child of 3rd row in tree store
    path = Gtk.TreePath([2, 4])
    treeiter = treestore.get_iter(path)
    # Get value at 2nd column
    value = treestore.get_value(treeiter, 1)

:class:`Gtk.TreePath` 的实例可以想list那样访问，例如
``len(treepath)`` 返回 ``treepath`` 指向的节点的深度，而 ``treepath【i】`` 则返回第i层的孩子的索引。

TreeModel 对象
^^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeModel()

    .. method:: get_iter(path)

        返回指向 *path* 的 :class:`Gtk.TreeIter` 的实例。

        *path* 应该是逗号分割的数字组成的字符串或者数组元组。例如，字符串 "10:4:0" 创建的path有三层，
        指向根节点的第11个孩子，的第五个孩子，的第一个孩子。有点儿绕～～

    .. method:: iter_next(treeiter)

        返回指向当前level的下一个节点的 :class:`Gtk.TreeIter` 的实例，如果没有下一个则返回 ``None`` 。

    .. method:: iter_previous(treeiter)

        饭或指向当前level的前一个节点的 :class:`Gtk.TreeIter` 的实例，如果没有前一个节点则返回 ``None`` 。

    .. method:: iter_has_child(treeiter)

        如果 *treeiter* 有孩子则返回 ``True`` ，否则返回 ``False`` 。

    .. method:: iter_children(treeiter)

        返回一个指向treeiter的第一个孩子的 :class:`Gtk.TreeIter` 的实例，或者如果没有孩子则返回 ``None`` 。

    .. method:: get_iter_first()

        返回指向树的第一个节点的（path “0” 的那个节点） :class:`Gtk.TreeIter` 的实例，或者如果为空树则返回 ``None`` 。

ListStore 对象
^^^^^^^^^^^^^^^^^

.. class:: Gtk.ListStore(data_type[, ...])

    创建一个新的 :class:`Gtk.ListStore` ，参数指定每一列的数据类型。添加到ListStore的每一行都要在每一列有相应的数据。

    支持的数据类型包括标准的Python类型和GTK+的类型：

    * str, int, float, long, bool, object
    * GObject.GObject

    .. method:: append([row])

    向ListStore中添加一个新行。

    *row* 是一个包含每列数据的列表，即 ``len(store) == len(row)`` 。
    如果 *row* 忽略或者传递 ``None`` ，则添加一个空行。

    返回指向新添加的行的 :class:`Gtk.TreeIter` 的实例。

TreeStore 对象
^^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeStore(data_type[, ...])

    参数与 :class:`Gtk.ListStore` 的构造函数一样。

    .. method:: append(parent, [row])

    向TreeStore中添加一新行数据。 *parent* 必须是一个有效的 :class:`Gtk.TreeIter` 。如果
    *parent* 不为 ``None`` ，会在 *parent* 的最后一个孩子后面添加一个新行，否则会在顶层添加一行。

    *row* 是一个包含每列数据的列表，即 ``len(store) == len(row)`` 。
    如果 *row* 忽略或者传递 ``None`` ，则添加一个空行。

    返回指向新添加的行的 :class:`Gtk.TreeIter` 的实例。

TreePath 对象
^^^^^^^^^^^^^^^^

.. class:: Gtk.TreePath(path)

    构造一个指向由 *path* 指定的节点的 :class:`Gtk.TreePath` 的实例。

    如果 *path* 为字符串，则要求是冒号分割的数字列表。例如，字符串 "10:4:0" 创建了一个三层深的path，
    指向根节点的第11个孩子，的第五个孩子，的第一个孩子。又来了。。。

    如果 *path* 为一个列表list或元组tuple，则要包含节点的索引，
    参照上面的例子，表达式 ``Gtk.TreePath("10:4:0")`` 与 ``Gtk.TreePath([10, 4, 3])`` 等效。

The View（视图）
--------------------------
尽管有很多不同的模型可以选择，但只有一个视图控件。这个视图控件可以与list或者tree store一起工作。
设置好一个 :class:`Gtk.TreeView` 并不是一件困难的事：可以通过构造函数或者调用:meth:`Gtk.TreeView.set_model`
来创建一个:class:`Gtk.TreeModel` 的实例来获取数据。

.. code-block:: python

    tree = Gtk.TreeView(store)

一旦 :class:`Gtk.TreeView` 控件有了一个模型之后，它还需要知道如何显示这个模型，一般是通过列和单元格渲染器（cell renderer）来完成。

Cell renderer 用来以一种方式将数据展现在tree model中。GTK+自带了很多的cell renderer，例如：
:class:`Gtk.CellRendererText` ， :class:`Gtk.CellRendererPixbuf` 和
:class:`Gtk.CellRendererToggle`.
另外，相对来说很容易自己定制一个renderer。

:class:`Gtk.TreeViewColumn` 是 :class:`Gtk.TreeView` 用来在tree iew中组织一列数据的对象。
一般需要列名作为标签显示给用户，要用那种的单元格渲染器，及从模型中获取哪一些数据这些参数。

.. code-block:: python

    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Title", renderer, text=0)
    tree.append_column(column)

要在一列中渲染多列model中的数据的话，你需要创建一个
:class:`Gtk.TreeViewColumn` 的实例并使用 :meth:`Gtk.TreeViewColumn.pack_start`
来添加model的列。

.. code-block:: python

    column = Gtk.TreeViewColumn("Title and Author")

    title = Gtk.CellRendererText()
    author = Gtk.CellRendererText()

    column.pack_start(title, True)
    column.pack_start(author, True)

    column.add_attribute(title, "text", 0)
    column.add_attribute(author, "text", 1)

    tree.append_column(column)

TreeView 对象
^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeView([treemodel])

    创建一个新的 :class:`Gtk.TreeView` 控件，其model初始化为
    *treemodel* 。 *treemodel* 必须是一个实现了 :class:`Gtk.TreeModel` 的类，例如
    :class:`Gtk.ListStore` 或者 :class:`Gtk.TreeStore` 。如果 *treemodel*
    忽略了或者传递 ``None`` ，model保持未设置状态并且你后面需要调用
    :meth:`set_model` 来设置。

    .. method:: set_model(model)

        设置tree iew的model。如果之前已经设置了一个model，那么会替换掉原来的，如果 *model* 为
        ``None`` ，则会清除掉原来旧的model。

    .. method:: get_model()

        返回tree view的model。如果之前没有设置model则返回 ``None`` 。

    .. method:: append_column(column)

        添加 *column* 到列列表中，即添加新的一列吧。

    .. method:: get_selection()

        返回与tree view关联的 :class:`Gtk.TreeSelection` 。

    .. method:: enable_model_drag_source(start_button_mask, targets, actions)

        参数与 :meth:`Gtk.Widget.drag_source_set` 相同。

    .. method:: enable_model_dest_source(targets, actions)

        参数与 :meth:`Gtk.Widget.drag_dest_set` 相同。

TreeViewColumn 对象
^^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeViewColumn(label[, renderer[, **kwargs]])

    创建一个 :class:`Gtk.TreeViewColumn` 。

    *renderer* 为 :class:`Gtk.CellRenderer` 的实例，
    *kwargs* 键值对指定 *renderer* 的属性的默认值。这与对每一个键值对调用
    :meth:`pack_start` 和 :meth:`add_attribute` 的效果一样。

    如果 *renderer* 忽略，你需要手动调用 :meth:`pack_start` 或者
    :meth:`pack_end` 。

    .. method:: add_attribute(renderer, attribute, value)

        添加一个映射给这一列的属性。

        将value设置给 *renderer* 的 *attribute* 属性。例如模型的第二列包含字符串，你可以
        给 :class:`Gtk.CellRendererText` 设置 "text" 属性来获取第二列的值。

    .. method:: pack_start(renderer, expand)

        打包 *renderer* 到这一列的开始。如果 expand为 ``False`` ， *renderer* 只会分配需要的空间的大小。
        如果expand为 ``True`` ，那未使用的控件会平均的分配给各个单元格。

    .. method:: pack_end(renderer, expand)

        打包 *renderer* 到这一列的最后。如果 expand为 ``False`` ， *renderer* 只会分配需要的空间的大小。
        如果expand为 ``True`` ，那未使用的控件会平均的分配给各个单元格。

    .. method:: set_sort_column_id(sort_column_id)

        设置模型的哪一列用来给视图的这一列排序，这同时使得本列的列头可以点击。

    .. method:: get_sort_column_id()

        返回由 :meth:`Gtk.TreeViewColumn.set_sort_column_id` 设置的id。

    .. method:: set_sort_indicator(setting)

        设置是否在列头显示一个小箭头。

        *setting* 可以为 ``True`` （显示提示） 或者 ``False`` 。

    .. method:: get_sort_indicator()

        返回 :meth:`Gtk.TreeViewColumn.set_sort_indicator` 设置的值。

    .. method:: set_sort_order(order)

        改变本列的排序方式。

        *order* 可以是 ``Gtk.SortType.ASCENDING`` 或者 ``Gtk.SortType.DESCENDING`` 。

    .. method:: get_sort_order()

        返回 :meth:`Gtk.TreeViewColumn.set_sort_order` 设置的值。

The Selection
-------------
绝大多数应用不仅需要处理显示数据的问题，也需要从用户那里接受输入事件。
要接受输入时间，只要创建一个selection对象的引用并且连接到 "changed" 信号。

.. code-block:: python

    select = tree.get_selection()
    select.connect("changed", on_tree_selection_changed)

如下代码获取返回选中行的数据：

.. code-block:: python

    def on_tree_selection_changed(selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]

你可通过调用 :meth:`Gtk.TreeSelection.set_mode` 来控制哪种选择被允许。
如果你将mode设置为 :attr:`Gtk.SelectionMode.MULTIPLE` ，那么
:meth:`Gtk.TreeSelection.get_selected` 就不能工作了，你需要调用
:meth:`Gtk.TreeSelection.get_selected_rows` 。


TreeSelection 对象
^^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeSelection

    .. method:: set_mode(type)

        type的值为以下其一：

        * :attr:`Gtk.SelectionMode.NONE`: 不可选。
        * :attr:`Gtk.SelectionMode.SINGLE`: 零或一个项目可以选中。
        * :attr:`Gtk.SelectionMode.BROWSE`: 有且只有一个项目可被选中。
          在某些环境，例如在初始化或搜索操作时，是可能没有项目可以选中的。
          必须选中是强调用户不能取消当前选中的项目——除非选择了一个新的项目。
        * :attr:`Gtk.SelectionMode.MULTIPLE`: 任意数量的项目可以被选中。
          点击会改变项目的选中状态。Ctrl键可以用来多选，Shift键用来选择一个范围。
          一些控件也允许点击然后拖拽来选择一个范围内的项目。

    .. method:: get_selected()

        返回 ``(model, treeiter)`` 的元组， *model* 是当期的模型， *treeiter* 是
        :class:`Gtk.TreeIter` 的一个实例并且指向当前选中的行。如果没有行被选中，
        *treeiter* 为 ``None`` 。

        如果选择的模式为 :attr:`Gtk.SelectionMode.MULTIPLE` 此函数将不能工作。

    .. method:: get_selected_rows()

        返回所有选中行的 :class:`Gtk.TreePath` 的实例的列表。

排序
-------
排序对于tree view是一个重要的特性，并且标准的实现了
:class:`Gtk.TreeSortable` 接口的tree model（
:class:`Gtk.TreeStore` and :class:`Gtk.ListStore` ）就支持排序。

通过点击列标题排序
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:class:`Gtk.TreeView` 的列通过调用
:meth:`Gtk.TreeViewColumn.set_sort_column_id` 可以很容易的实现排序。
之后这一列就可以通过单击标题来排序了。

首先我们需要一个简单的 :class:`Gtk.TreeView` 和其模型 :class:`Gtk.ListStore` 。

.. code-block:: python

    model = Gtk.ListStore(str)
    model.append(["Benjamin"])
    model.append(["Charles"])
    model.append(["alfred"])
    model.append(["Alfred"])
    model.append(["David"])
    model.append(["charles"])
    model.append(["david"])
    model.append(["benjamin"])

    treeView = Gtk.TreeView(model)

    cellRenderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Title", renderer, text=0)

下一步就是是能排序。注意 *column_id* （例子中为 ``0`` ）指模型中的列而 **不是** 视图中的列。

.. code-block:: python

    column.set_sort_column_id(0)

设置一个定制的排序函数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
当然你也可以定制一个比较函数来改变排序的行为。例子中我们创建一个
比较函数来实现大小写敏感的排序功能。
上面的例子排序后的列表像下面这样：::

    alfred
    Alfred
    benjamin
    Benjamin
    charles
    Charles
    david
    David

大小写敏感的排序排序后的列表像这样：::

    Alfred
    Benjamin
    Charles
    David
    alfred
    benjamin
    charles
    david

首先一个我们需要一个比较函数。这个函数需要两个行，
并且如果第一个行应该排在前面返回负数，
如果两个行的比较结果相等返回0，如果第二个行应该排在前面则返回一个正数。

.. code-block:: python

    def compare(model, row1, row2, user_data):
        sort_column, _ = model.get_sort_column_id()
        value1 = model.get_value(row1, sort_column)
        value2 = model.get_value(row2, sort_column)
        if value1 < value2:
            return -1
        elif value1 == value2:
            return 0
        else:
            return 1

排序函数需要通过 :meth:`Gtk.TreeSortable.set_sort_func` 来设置。

.. code-block:: python

    model.set_sort_func(0, compare, None)

TreeSortable 对象
^^^^^^^^^^^^^^^^^^^^

.. class:: Gtk.TreeSortable()

    .. method:: set_sort_column_id(sort_column_id, order)

        设置当前的排序列为 *sort_column_id* 。

        *order* 可以为 ``Gtk.SortType.ASCENDING`` 或者 ``Gtk.SortType.DESCENDING`` 。

    .. method:: get_sort_column_id()

        返回一个包含当前排序列和排序方法的元组。

    .. method:: set_sort_func(sort_column_id, sort_func, user_data)

        设置用来通过 *sort_column_id* 来排序时的比较函数。

        *user_data* 会传递给 *sort_func* 。

        *sort_func* 是一个原型为 ``sort_func(model, iter1, iter2, user_data)`` 的函数。
        并且在 *iter1* 应该排在 *iter2* 前时返回一个负数，相等时返回0，
        *iter2* 应该排在  *iter1* 前时返回一个正数。

    .. method:: set_default_sort_func(sort_func, user_data)

        参见 :meth:`Gtk.TreeSortable.set_sort_func` 。用来设置当使用默认的排序列时使用的比较函数。
