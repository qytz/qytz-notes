.. _context:

*************
Cairo Context
*************

.. currentmodule:: cairo

.. comment block
   example reST:
   (add back '..' where required at column 0)
 . class:: module.C[(signature)]
   .. classmethod:: name(signature)
   .. staticmethod:: name(signature)
   .. method:: method(signature)

      :param p1: xxx
      :type p1: int
      :param p2: xxx
      :type p2: str
      :returns: xxx
      :rtype: list of strings
      :raises: xxx

      .. versionadded:: 1.6
   links:
     :data:`cairo.ANTIALIAS_SUBPIXEL`
     :class:`Context`
     :exc:`cairo.Error`
     :meth:`.copy_page`
     :meth:`Context.copy_page`
     :ref:`LINE_CAP <constants_LINE_CAP>`


class Context()
===============

*Context* 是你使用cairo绘制时主要用到的对象。当你要使用cairo绘制时，你首先创建一个
*Context* 上下文，设置目标surface及上下文的选项，调用 :meth:`Context.move_to` 等方法
创建shape形状，然后调用 :meth:`Context.stroke` 或者 :meth:`Context.fill` 将形状绘制到surface。

*Contexts* 可以通过 :meth:`Context.save` 保存到栈上，然后你就可以安全的修改上下文而不用担心丢失任何状态了。
完成之后调用 :meth:`Context.restore` 来恢复之前保存的状态。

.. class:: Context(target)

   :param target: 上下文的目标 :class:`Surface`
   :returns: 一个新分配的上下文
   :raises: 没有内存时产生 *MemoryError* 异常

   创建一个新的 *Context* ，所有的状态参数设置为默认值，并以 *target* 作为目地surface，目的surface应该使用
   后端特定的函数来构建，比如： :class:`ImageSurface` （或者其他的cairo后端surface的构造函数）

   .. method:: append_path(path)

      :param path: :class:`Path` to be appended

      将 *path* 添加到当前的路径path。 *path* 可以是由
      :meth:`Context.copy_path` 或者 :meth:`Context.copy_path_flat` 返回，也可能是手动构建的（使用C语言）。

   .. method:: arc(xc, yc, radius, angle1, angle2)

      :param xc: 圆心的X坐标
      :type xc: float
      :param yc: 圆心的Y坐标
      :type yc: float
      :param radius: 圆的半径
      :type radius: float
      :param angle1: 起始角度，以弧度表示
      :type angle1: float
      :param angle2: 结束角度，以弧度表示
      :type angle2: float

      以给定的半径 *radius* 在当前的path路径上添加一个圆弧。圆弧以(*xc, yc*)为圆心，以 *angle1* 角度为起始点，
      按照角度增加的方向直到 *angle2* 结束，如果 *angle2* 小于 *angle1* ，则会绘制整个的圆（角度增长 2*PI 直到大于 *angle1* ）。

      如果有一个当前的点，那么一条从当前点到圆弧起点的线段会添加到路径。
      如果你不想绘制这条线段，可以在调用 :meth:`Context.arc` 之前先调用 :meth:`Context.new_sub_path` 。

      角度以弧度为单位。角度0是X轴的正方向（user space），角度PI/2.0（90度）是Y轴的正方向（user space），角度从
      X轴方向到Y轴正方向的方向增长，因此在默认的转换矩阵（default transformation matrix）下角度以顺时针方向增长。

      要从角度转换到弧度，使用 ``degrees * (math.pi / 180)`` 。

      本函数以角度正向增长的方向绘制圆弧，如果需要向相反的方向绘制请参考：
      :meth:`Context.arc_negative` 。
      
      圆弧的绘制在user space是圆形的。要想绘制椭圆，你可以在X和Y方向以不同的数量缩放（scale）当前的转换矩阵（current transformation matrix）。
      例如要绘制 \*x, y, width, height 大小的椭圆，可以使用如下的代码::

        ctx.save()
        ctx.translate(x + width / 2., y + height / 2.)
        ctx.scale(width / 2., height / 2.)
        ctx.arc(0., 0., 1., 0., 2 * math.pi)
        ctx.restore()


   .. method:: arc_negative(xc, yc, radius, angle1, angle2)

      :param xc: 圆弧圆心X坐标
      :type xc: float
      :param yc: 圆弧圆心Y坐标
      :type yc: float
      :param radius: 圆弧的半径
      :type radius: float
      :param angle1: 圆弧的起始角度
      :type angle1: float
      :param angle2: 圆弧的结束角度
      :type angle2: float

      以给定的半径 *radius* 在当前的path路径上添加一个圆弧。圆弧以(*xc, yc*)为圆心，以 *angle1* 角度为起始点，
      按照角度减小的方向直到 *angle2* 结束，如果 *angle2* 大于 *angle1* ，则会绘制整个的圆（角度减小 2*PI 直到小于 *angle1* ）。

      详细信息参考 :meth:`Context.arc` 。这两个函数唯一的不同在于两个角度间圆弧的方向。

   .. method:: clip()

      使用当前的path路径建立一个新的裁切区域，旧的裁切区域会根据当前的
      :ref:`FILL RULE <constants_FILL_RULE>` （参考 :meth:`Context.set_fill_rule` ）
      调用 :meth:`Context.fill` 填充。

      调用 :meth:`.clip` 后当前的路径path会从 :class:`Context` 清除。

      裁切区域会影响所有的绘制操作——掩盖掉所有在当前绘制区域之外的改变。

      调用 :meth:`.clip` 只能创建更小的裁切区域，无法创建更大大的裁切区域。
      但是当前裁切区域也是绘制状态（graphics state）的一部分，因此通过 :meth:`.clip`
      创建临时的裁切区域前后，你可能需要调用 :meth:`Context.save`/:meth:`Context.restore` 。
      其他的增加裁切区域的方法只有 :meth:`Context.reset_clip` 。
     
   .. method:: clip_extents()

      :returns: (x1, y1, x2, y2)
      :rtype: (float, float, float, float)

      * *x1*: 返回范围的左边界
      * *y1*: 返回范围的顶部边界
      * *x2*: 返回范围的右边界
      * *y2*: 返回范围的底部边界

      计算覆盖当前裁切区域的一个边界范围的坐标。

      .. versionadded:: 1.4

   .. method:: clip_preserve()

      使用当前的path路径建立一个新的裁切区域，旧的裁切区域会根据当前的
      :ref:`FILL RULE <constants_FILL_RULE>` （参考 :meth:`Context.set_fill_rule` ）
      调用 :meth:`Context.fill` 填充。

      与 :meth:`Context.clip` 不同， :meth:`.clip_preserve` 会保存 :class:`Context` 的当前路径path。
      
      裁切区域会影响所有的绘制操作——掩盖掉所有在当前绘制区域之外的改变。

      调用  :meth:`.clip_preserve` 只能创建更小的裁切区域，无法创建更大大的裁切区域。
      但是当前裁切区域也是绘制状态（graphics state）的一部分，因此通过 :meth:`.clip`
      创建临时的裁切区域前后，你可能需要调用 :meth:`Context.save`/:meth:`Context.restore` 。
      其他的增加裁切区域的方法只有 :meth:`Context.reset_clip` 。
     
   .. method:: close_path()

      从当前点（最近调用 :meth:`Context.move_to` 传递的点）到当前子路径的起点添加一条线段，
      闭合当前的子路径。调用完成之后，连接到的子路径的断点成为新的当前点。

      在一次绘制stroke时，
      :meth:`.close_path` 的行为与以等价的终点坐标调用 :meth:`Context.line_to` 并不相同。
      闭合的子路径在一次绘制stroke时，
      在子路径的终点并没有'盖'（cap）（译注：见 :ref:`cairo.LINE_CAP <constants_LINE_CAP>` ），
      而是使用线段连接line join（译注：见 :ref:`cairo.LINE_CAP <constants_LINE_JOIN>` ）将子路径
      的起点和终点连接起来。

      如果在调用 :meth:`.close_path` 时没有当前绘制点（current point），调用将没有任何效果。

      Note: 1.2.4版本的cairo在任何调用 :meth:`.close_path` 时在路径闭合后都会执行 MOVE_TO，
      （例子参考 :meth:`Context.copy_path` ）。这在某些情况下可以简化路径的处理——因为这样在处理时
      就不用保存最后移动到的点了，因为 MOVE_TO 会提供这个点。

   .. method:: copy_clip_rectangle_list()

      :returns: 当前裁切区域的矩形坐标列表
      :rtype: 四个浮点数的元组的列表

      (列表中的 status 可能是 %CAIRO_STATUS_CLIP_NOT_REPRESENTABLE ，意指裁切区域不能用一个用户态矩形（user-space rectangles）代表。
      status 也可能是指代其他错误的值。——pycairo中未实现）

      .. versionadded:: 1.4

   .. method:: copy_page()

      对于支持多页操作的后端，发射（emits，疑应翻译为显示？）当前页，但是内容并不会被清除，因此当前页的内容会保留给下一个页。
      如果你想在发射后得到一个空的页，需要调用 :meth:`Context.show_page` 。

      本函数是一个便捷函数，只是调用了 *Context* 的目标设备的 :meth:`Surface.copy_page` 函数。

   .. method:: copy_path()

      :returns: :class:`Path`
      :raises: 没有内存时触发 *MemoryError* 异常

      创建当前路径的一个拷贝并且以  :class:`Path` 返回给用户。

   .. method:: copy_path_flat()

      :returns: :class:`Path`
      :raises: 没有内存时触发 *MemoryError* 异常

      获取当前路径的一个 flattened 的拷贝并且以 :class:`Path` 返回给用户。

      本函数与 :meth:`Context.copy_path` 类似，但是路径中所有的曲线都以分段线性的方式被线性化
      （使用当前的容错值，current tolerance value）。即结果肯定不含有CAIRO_PATH_CURVE_TO类型的元素，
      所有这种类型的元素都被替换为一系列的CAIRO_PATH_LINE_TO元素了。

   .. method:: curve_to(x1, y1, x2, y2, x3, y3)

      :param x1:第一个控制点的X坐标
      :type x1: float
      :param y1: 第一个控制点的Y坐标
      :type y1: float
      :param x2: 第二个控制点的X坐标
      :type x2: float
      :param y2: 第二个控制点的Y坐标
      :type y2: float
      :param x3: 第三个控制点的X坐标
      :type x3: float
      :param y3: 第三个控制点的Y坐标
      :type y3: float

      从当前点到 *(x3, y3)* 点添加一条贝塞尔曲线（cubic Bézier spline），使用 *(x1, y1)* 和
      *(x2, y2)* 作为控制点。坐标均未用户态的值，调用完成之后当前点移动到 *(x3, y3)* 。

      如果在调用 :meth:`.curve_to` 当前点没有被设置，函数的行为类似于调用 ``ctx.move_to(x1, y1)`` 函数。

   .. method:: device_to_user(x, y)

      :param x: 坐标的X值
      :type x: float
      :param y: 坐标的Y值
      :type y: float
      :returns: (x, y)
      :rtype: (float, float)

      通过将给定点乘以前转换矩阵（current transformation matrix，CTM）的逆矩阵将设备空间的坐标转换为用户空间的坐标。

   .. method:: device_to_user_distance(dx, dy)

      :param dx: 距离向量的X值
      :type dx: float
      :param dy: 距离向量的Y值
      :type dy: float
      :returns: (dx, dy)
      :rtype: (float, float)

      将设备空间的距离向量转换到用户空间。
      本函数与 :meth:`Context.device_to_user` 类似，但是CTM的逆矩阵的转换相关部分（translation components）会被忽略。

   .. method:: fill()

      根据当前的填充规则（:ref:`FILL RULE <constants_FILL_RULE>`）填充当前路径的一个绘制操作，在绘制前，所有的子路径都被隐式的闭合了。
      在调用 :meth:`.fill` 之后，当前的路径会从 class:`Context` 清除。请参考 :meth:`Context.set_fill_rule`
      和 :meth:`Context.fill_preserve` 。

   .. method:: fill_extents()

      :returns: (x1, y1, x2, y2)
      :rtype: (float, float, float, float)

      * *x1*: 返回填充延展区域的左边界
      * *y1*: 返回填充延展区域的上边界
      * *x2*: 返回填充延展区域的右边界
      * *y2*: 返回填充延展区域的下边界

      计算当前路径的 :meth:`Context.fill` 操作会影响（即填充）的区域的边界盒子的用户空间坐标。
      如果当前路径为空，则返回一个空的矩形(0,0,0,0)，surface区域和裁切并未考虑在内（Surface dimensions and）。

      与 :meth:`Context.path_extents` 的区别是  :meth:`Context.path_extents`  对于没有填充区域的一些路径（例如一条简单的线段）返回
      非零的扩展区域。

      请注意 :meth:`.fill_extents` 函数需要做更多的操作才能计算出精确的填充操作被填充的的区域的大小，
      因此对于性能要求比较高的地方 :meth:`Context.path_extents` 可能更适合。

      参考 :meth:`Context.fill` ， :meth:`Context.set_fill_rule` 和
      :meth:`Context.fill_preserve`.

   .. method:: fill_preserve()

      根据当前的填充规则（:ref:`FILL RULE <constants_FILL_RULE>`）填充当前路径的一个绘制操作，在绘制前，所有的子路径都被隐式的闭合了。
      但是不像 :meth:`Context.fill` ，:meth:`.fill_preserve` 会保留 :class:`Context` 的路径。

      参考 :meth:`Context.set_fill_rule` and :meth:`Context.fill`.

   .. method:: font_extents()

      :returns: (ascent, descent, height, max_x_advance, max_y_advance)
      :rtype: (float, float, float, float, float)

      获取当前选择字体的延展区域（extents）。

   .. method:: get_antialias()

      :returns: 当前的 :ref:`ANTIALIAS <constants_ANTIALIAS>` 模式（由 :meth:`Context.set_antialias` 设置）。

   .. method:: get_current_point()

      :returns: (x, y)
      :rtype: (float, float)

      * *x*: 当前点的X坐标
      * *y*: 当前点的Y坐标

      获取当前路径的当前点，理论上来讲就是路径目前的终点。

      返回当前点的用户态坐标。如果没有当前点，或者 :class:`Context` 处在一个错误的状态，
      *x* 和 *y* 都返回0.0。 可以通过  :meth:`Context.has_current_point` 来检查当前点。

      绝大多数的路径构建函数都会修改当前点的位置，参考以下函数以了解这些操作对当前点的详细影响：
      :meth:`Context.new_path`, :meth:`Context.new_sub_path`,
      :meth:`Context.append_path`, :meth:`Context.close_path`,
      :meth:`Context.move_to`, :meth:`Context.line_to`,
      :meth:`Context.curve_to`, :meth:`Context.rel_move_to`,
      :meth:`Context.rel_line_to`, :meth:`Context.rel_curve_to`,
      :meth:`Context.arc`, :meth:`Context.arc_negative`,
      :meth:`Context.rectangle`, :meth:`Context.text_path`,
      :meth:`Context.glyph_path`, :meth:`Context.stroke_to_path`.

      以下函数会修改当前点但是并不改变当前的路径：
      :meth:`Context.show_text`.

      以下函数会删除（unset）当前的路径，因此也会删除单签点：
      :meth:`Context.fill`, :meth:`Context.stroke`.

   .. method:: get_dash()

      :returns: (dashes, offset)
      :rtype: (tuple, float)

      * *dashes*: dash数组
      * *offset*: 当前dash的偏移值。

      获取当前的dash数组。

      .. versionadded:: 1.4

   .. method:: get_dash_count()

      :returns: dash数组的长度，如果dash数组没有被设置则返回0。
      :rtype: int

      参考 :meth:`Context.set_dash` 和 :meth:`Context.get_dash`.

      .. versionadded:: 1.4

   .. method:: get_fill_rule()

      :returns: 当前的 :ref:`FILL RULE <constants_FILL_RULE>` （由 :meth:`Context.set_fill_rule` 函数设置）。

   .. method:: get_font_face()

      :returns: :class:`Context` 当前的 :class:`FontFace` 。

   .. method:: get_font_matrix()

      :returns: :class:`Context` 当前的 :class:`Matrix` 。

      参考 :meth:`Context.set_font_matrix`.

   .. method:: get_font_options()

      :returns: :class:`Context` 当前的 :class:`FontOptions` 。

      获取 :meth:`Context.set_font_options` 设置的字体渲染选项。
      注意返回的选项并不包含从底层surface继承的选项；从字面意思来看返回的就是
      传递给 :meth:`Context.set_font_options`  的选项。

   .. method:: get_group_target()

      :returns: the target :class:`Surface`.

      返回 :class:`Context` 的当前目的 :class:`Surface` ，或者是传递给 :class:`Context` 的
      原来的目的，或者是最近调用 :meth:`Context.push_group` 或者 :meth:`Context.push_group_with_content`
      设置的当前组的目的surface。

      .. versionadded:: 1.2

   .. method:: get_line_cap()

      :returns: 当前的 :ref:`LINE_CAP <constants_LINE_CAP>` 风格，由 :meth:`Context.set_line_cap` 设置。

   .. method:: get_line_join()

      :returns: 当前的 :ref:`LINE_JOIN <constants_LINE_JOIN>` 风格，由
        :meth:`Context.set_line_join` 设置。

   .. method:: get_line_width()

      :returns: 当前的线宽
      :rtype: float

      本函数返回由 :meth:`Context.set_line_width` 设置的当前的线宽。
      注意即使CTM在调用 :meth:`Context.set_line_width` 之后已经被改变，返回的值也不变。

   .. method:: get_matrix()

      :returns: 当前转换矩阵 :class:`Matrix` (CTM)

   .. method:: get_miter_limit()

      :returns: 当前的斜切限制，由
        :meth:`Context.set_miter_limit` 设置。
      :rtype: float

   .. method:: get_operator()

      :returns: :class:`Context` 的当前合成操作 :ref:`OPERATOR <constants_OPERATOR>` 。

   .. method:: get_scaled_font()

      :returns: :class:`Context` 当前的 :class:`ScaledFont` 。

      .. versionadded:: 1.4

   .. method:: get_source()

      :returns: :class:`Context` 的当前pattern源 :class:`Pattern` 。

   .. method:: get_target()

      :returns: :class:`Context` 的目的surface :class:`Surface` 。

   .. method:: get_tolerance()

      :returns: 当前的容错值（the current tolerance value），由
        :meth:`Context.set_tolerance` 设置。
      :rtype: float

   .. method:: glyph_extents(glyphs, [num_glyphs])

      :param glyphs: glyphs
      :type glyphs: a sequence of (int, float, float)
      :param num_glyphs: number of glyphs to measure, defaults to using all
      :type num_glyphs: int
      :returns: x_bearing, y_bearing, width, height, x_advance, y_advance
      :rtype: 6-tuple of float

      Gets the extents for an array of glyphs. The extents describe a
      user-space rectangle that encloses the "inked" portion of the glyphs,
      (as they would be drawn by :meth:`Context.show_glyphs`). Additionally,
      the x_advance and y_advance values indicate the amount by which the
      current point would be advanced by :meth:`Context.show_glyphs`.

      Note that whitespace glyphs do not contribute to the size of the
      rectangle (extents.width and extents.height).

   .. method:: glyph_path(glyphs[, num_glyphs])

      :param glyphs: glyphs to show
      :type glyphs: a sequence of (int, float, float)
      :param num_glyphs: number of glyphs to show, defaults to showing all
      :type num_glyphs: int

      Adds closed paths for the glyphs to the current path. The generated path
      if filled, achieves an effect similar to that of
      :meth:`Context.show_glyphs`.

   .. method:: has_current_point()

      returns: True iff a current point is defined on the current path.
        See :meth:`Context.get_current_point` for details on the current point.

      .. versionadded:: 1.6

   .. method:: identity_matrix()

      Resets the current transformation :class:`Matrix` (CTM) by setting it
      equal to the identity matrix. That is, the user-space and device-space
      axes will be aligned and one user-space unit will transform to one
      device-space unit.

   .. method:: in_fill(x, y)

      :param x: 测试点的X坐标
      :type x: float
      :param y: 测试点的Y坐标
      :type y: float
      :returns: 如果该点在当前路径的 :meth:`Context.fill` 操作的影响区域内返回True，
        surface的尺寸和裁切并没有考虑在内。

      参考 :meth:`Context.fill` ， :meth:`Context.set_fill_rule` 和
      :meth:`Context.fill_preserve` 。

   .. method:: in_stroke(x, y)

      :param x: X coordinate of the point to test
      :type x: float
      :param y: Y coordinate of the point to test
      :type y: float

      :returns: True iff the point is inside the area that would be affected
        by a :meth:`Context.stroke` operation given the current path and
        stroking parameters. Surface dimensions and clipping are not taken
        into account.

      See :meth:`Context.stroke`, :meth:`Context.set_line_width`,
      :meth:`Context.set_line_join`, :meth:`Context.set_line_cap`,
      :meth:`Context.set_dash`, and :meth:`Context.stroke_preserve`.

   .. method:: line_to(x, y)

      :param x: the X coordinate of the end of the new line
      :type x: float
      :param y: the Y coordinate of the end of the new line
      :type y: float

      Adds a line to the path from the current point to position *(x, y)* in
      user-space coordinates. After this call the current point will be *(x,
      y)*.

      If there is no current point before the call to :meth:`.line_to`
      this function will behave as ``ctx.move_to(x, y)``.

   .. method:: mask(pattern)

      :param pattern: a :class:`Pattern`

      A drawing operator that paints the current source using the alpha
      channel of *pattern* as a mask. (Opaque areas of *pattern* are painted
      with the source, transparent areas are not painted.)

   .. method:: mask_surface(surface, x=0.0, y=0.0)

      :param surface: a :class:`Surface`
      :param x: X coordinate at which to place the origin of *surface*
      :type x: float
      :param y: Y coordinate at which to place the origin of *surface*
      :type y: float

      A drawing operator that paints the current source using the alpha
      channel of *surface* as a mask. (Opaque areas of *surface* are painted
      with the source, transparent areas are not painted.)

   .. method:: move_to(x, y)

      :param x: the X coordinate of the new position
      :type x: float
      :param y: the Y coordinate of the new position
      :type y: float

      Begin a new sub-path. After this call the current point will be *(x,
      y)*.

   .. method:: new_path()

      Clears the current path. After this call there will be no path and no
      current point.

   .. method:: new_sub_path()

      Begin a new sub-path. Note that the existing path is not affected. After
      this call there will be no current point.

      In many cases, this call is not needed since new sub-paths are
      frequently started with :meth:`Context.move_to`.

      A call to :meth:`.new_sub_path` is particularly useful when beginning a
      new sub-path with one of the :meth:`Context.arc` calls. This makes
      things easier as it is no longer necessary to manually compute the arc's
      initial coordinates for a call to :meth:`Context.move_to`.

      .. versionadded:: 1.6

   .. method:: paint()

      A drawing operator that paints the current source everywhere within the
      current clip region.

   .. method:: paint_with_alpha(alpha)

      :param alpha: alpha value, between 0 (transparent) and 1 (opaque)
      :type alpha: float

      A drawing operator that paints the current source everywhere within the
      current clip region using a mask of constant alpha value *alpha*. The
      effect is similar to :meth:`Context.paint`, but the drawing is faded out
      using the alpha value.

   .. method:: path_extents()

      :returns: (x1, y1, x2, y2)
      :rtype: (float, float, float, float)

      * *x1*: left of the resulting extents
      * *y1*: top of the resulting extents
      * *x2*: right of the resulting extents
      * *y2*: bottom of the resulting extents

      Computes a bounding box in user-space coordinates covering the points on
      the current path. If the current path is empty, returns an empty
      rectangle (0, 0, 0, 0). Stroke parameters, fill rule, surface
      dimensions and clipping are not taken into account.

      Contrast with :meth:`Context.fill_extents` and
      :meth:`Context.stroke_extents` which return the extents of only the area
      that would be "inked" by the corresponding drawing operations.

      The result of :meth:`.path_extents` is defined as equivalent to the
      limit of :meth:`Context.stroke_extents` with cairo.LINE_CAP_ROUND as the
      line width approaches 0.0, (but never reaching the empty-rectangle
      returned by :meth:`Context.stroke_extents` for a line width of 0.0).

      Specifically, this means that zero-area sub-paths such as
      :meth:`Context.move_to`; :meth:`Context.line_to` segments, (even
      degenerate cases where the coordinates to both calls are identical),
      will be considered as contributing to the extents. However, a lone
      :meth:`Context.move_to` will not contribute to the results of
      :meth:`Context.path_extents`.

      .. versionadded:: 1.6

   .. method:: pop_group()

      :returns: a newly created :class:`SurfacePattern` containing the results
        of all drawing operations performed to the group.

      Terminates the redirection begun by a call to :meth:`Context.push_group`
      or :meth:`Context.push_group_with_content` and returns a new pattern
      containing the results of all drawing operations performed to the group.

      The :meth:`.pop_group` function calls :meth:`Context.restore`,
      (balancing a call to :meth:`Context.save` by the
      :meth:`Context.push_group` function), so that any changes to the graphics
      state will not be visible outside the group.

      .. versionadded:: 1.2

   .. method:: pop_group_to_source()

      Terminates the redirection begun by a call to :meth:`Context.push_group`
      or :meth:`Context.push_group_with_content` and installs the resulting
      pattern as the source :class:`Pattern` in the given :class:`Context`.

      The behavior of this function is equivalent to the sequence of
      operations::

        group = cairo_pop_group()
        ctx.set_source(group)

      but is more convenient as their is no need for a variable to store
      the short-lived pointer to the pattern.

      The :meth:`Context.pop_group` function calls :meth:`Context.restore`,
      (balancing a call to :meth:`Context.save` by the
      :meth:`Context.push_group` function), so that any changes to the graphics
      state will not be visible outside the group.

      .. versionadded:: 1.2

   .. method:: push_group()

      Temporarily redirects drawing to an intermediate surface known as a
      group. The redirection lasts until the group is completed by a call to
      :meth:`Context.pop_group` or :meth:`Context.pop_group_to_source`. These
      calls provide the result of any drawing to the group as a pattern,
      (either as an explicit object, or set as the source pattern).

      This group functionality can be convenient for performing intermediate
      compositing. One common use of a group is to render objects as opaque
      within the group, (so that they occlude each other), and then blend the
      result with translucence onto the destination.

      Groups can be nested arbitrarily deep by making balanced calls to
      :meth:`Context.push_group`/:meth:`Context.pop_group`. Each call
      pushes/pops the new target group onto/from a stack.

      The :meth:`.push_group` function calls :meth:`Context.save` so that any
      changes to the graphics state will not be visible outside the group,
      (the pop_group functions call :meth:`Context.restore`).

      By default the intermediate group will have a :ref:`CONTENT
      <constants_CONTENT>` type of cairo.CONTENT_COLOR_ALPHA. Other content
      types can be chosen for the group by using
      :meth:`Context.push_group_with_content` instead.

      As an example, here is how one might fill and stroke a path with
      translucence, but without any portion of the fill being visible
      under the stroke::

        ctx.push_group()
        ctx.set_source(fill_pattern)
        ctx.fill_preserve()
        ctx.set_source(stroke_pattern)
        ctx.stroke()
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)

      .. versionadded:: 1.2

   .. method:: push_group_with_content(content)

      :param content: a :ref:`CONTENT <constants_CONTENT>` indicating the
        type of group that will be created

      Temporarily redirects drawing to an intermediate surface known as a
      group. The redirection lasts until the group is completed by a call to
      :meth:`Context.pop_group` or :meth:`Context.pop_group_to_source`. These
      calls provide the result of any drawing to the group as a pattern,
      (either as an explicit object, or set as the source pattern).

      The group will have a content type of *content*. The ability to control
      this content type is the only distinction between this function and
      :meth:`Context.push_group` which you should see for a more detailed
      description of group rendering.

      .. versionadded:: 1.2

   .. method:: rectangle(x, y, width, height)

      :param x: the X coordinate of the top left corner of the rectangle
      :type x: float
      :param y: the Y coordinate to the top left corner of the rectangle
      :type y: float
      :param width: the width of the rectangle
      :type width: float
      :param height: the height of the rectangle
      :type height: float

      Adds a closed sub-path rectangle of the given size to the current path
      at position *(x, y)* in user-space coordinates.

      This function is logically equivalent to::

        ctx.move_to(x, y)
        ctx.rel_line_to(width, 0)
        ctx.rel_line_to(0, height)
        ctx.rel_line_to(-width, 0)
        ctx.close_path()

   .. method:: rel_curve_to(dx1, dy1, dx2, dy2, dx3, dy4)

      :param dx1: the X offset to the first control point
      :type dx1: float
      :param dy1: the Y offset to the first control point
      :type dy1: float
      :param dx2: the X offset to the second control point
      :type dx2: float
      :param dy2: the Y offset to the second control point
      :type dy2: float
      :param dx3: the X offset to the end of the curve
      :type dx3: float
      :param dy3: the Y offset to the end of the curve
      :type dy3: float
      :raises: :exc:`cairo.Error` if called with no current point.

      Relative-coordinate version of :meth:`Context.curve_to`. All
      offsets are relative to the current point. Adds a cubic Bézier spline to
      the path from the current point to a point offset from the current point
      by *(dx3, dy3)*, using points offset by *(dx1, dy1)* and *(dx2, dy2)* as
      the control points. After this call the current point will be offset by
      *(dx3, dy3)*.

      Given a current point of (x, y), ``ctx.rel_curve_to(dx1, dy1, dx2, dy2,
      dx3, dy3)`` is logically equivalent to ``ctx.curve_to(x+dx1, y+dy1,
      x+dx2, y+dy2, x+dx3, y+dy3)``.

   .. method:: rel_line_to(dx, dy)

      :param dx: the X offset to the end of the new line
      :type dx: float
      :param dy: the Y offset to the end of the new line
      :type dy: float
      :raises: :exc:`cairo.Error` if called with no current point.

      Relative-coordinate version of :meth:`Context.line_to`. Adds a line to
      the path from the current point to a point that is offset from the
      current point by *(dx, dy)* in user space. After this call the current
      point will be offset by *(dx, dy)*.

      Given a current point of (x, y), ``ctx.rel_line_to(dx, dy)`` is logically
      equivalent to ``ctx.line_to(x + dx, y + dy)``.

   .. method:: rel_move_to(dx, dy)

      :param dx: the X offset
      :type dx: float
      :param dy: the Y offset
      :type dy: float
      :raises: :exc:`cairo.Error` if called with no current point.

      Begin a new sub-path. After this call the current point will offset by
      *(dx, dy)*.

      Given a current point of (x, y), ``ctx.rel_move_to(dx, dy)`` is logically
      equivalent to ``ctx.(x + dx, y + dy)``.

   .. method:: reset_clip()

      Reset the current clip region to its original, unrestricted state. That
      is, set the clip region to an infinitely large shape containing the
      target surface. Equivalently, if infinity is too hard to grasp, one can
      imagine the clip region being reset to the exact bounds of the target
      surface.

      Note that code meant to be reusable should not call :meth:`.reset_clip`
      as it will cause results unexpected by higher-level code which calls
      :meth:`.clip`. Consider using :meth:`.save` and :meth:`.restore` around
      :meth:`.clip` as a more robust means of temporarily restricting the clip
      region.

   .. method:: restore()

      Restores :class:`Context` to the state saved by a preceding call to
      :meth:`.save` and removes that state from the stack of saved states.

   .. method:: rotate(angle)

      :param angle: angle (in radians) by which the user-space axes will be
        rotated
      :type angle: float

      Modifies the current transformation matrix (CTM) by rotating the
      user-space axes by *angle* radians. The rotation of the axes takes places
      after any existing transformation of user space. The rotation direction
      for positive angles is from the positive X axis toward the positive Y
      axis.

   .. method:: save()

      Makes a copy of the current state of :class:`Context` and saves it on an
      internal stack of saved states. When :meth:`.restore` is called,
      :class:`Context` will be restored to the saved state. Multiple calls to
      :meth:`.save` and :meth:`.restore` can be nested; each call to
      :meth:`.restore` restores the state from the matching paired
      :meth:`.save`.

   .. method:: scale(sx, sy)

      :param sx: scale factor for the X dimension
      :type sx: float
      :param sy: scale factor for the Y dimension
      :type sy: float

      Modifies the current transformation matrix (CTM) by scaling the X and Y
      user-space axes by *sx* and *sy* respectively. The scaling of the axes
      takes place after any existing transformation of user space.

   .. method:: select_font_face(family[, slant[, weight]])

      :param family: a font family name
      :type family: str
      :param slant: the :ref:`FONT_SLANT <constants_FONT_SLANT>` of the font,
        defaults to :data:`cairo.FONT_SLANT_NORMAL`.
      :param weight: the :ref:`FONT_WEIGHT <constants_FONT_WEIGHT>` of the
        font, defaults to :data:`cairo.FONT_WEIGHT_NORMAL`.

      Note: The :meth:`.select_font_face` function call is part of what the
      cairo designers call the "toy" text API. It is convenient for short
      demos and simple programs, but it is not expected to be adequate for
      serious text-using applications.

      Selects a family and style of font from a simplified description as a
      family name, slant and weight. Cairo provides no operation to list
      available family names on the system (this is a "toy", remember), but
      the standard CSS2 generic family names, ("serif", "sans-serif",
      "cursive", "fantasy", "monospace"), are likely to work as expected.

      For "real" font selection, see the font-backend-specific
      font_face_create functions for the font backend you are using. (For
      example, if you are using the freetype-based cairo-ft font backend, see
      cairo_ft_font_face_create_for_ft_face() or
      cairo_ft_font_face_create_for_pattern().) The resulting font face could
      then be used with cairo_scaled_font_create() and
      cairo_set_scaled_font().

      Similarly, when using the "real" font support, you can call directly
      into the underlying font system, (such as fontconfig or freetype), for
      operations such as listing available fonts, etc.

      It is expected that most applications will need to use a more
      comprehensive font handling and text layout library, (for example,
      pango), in conjunction with cairo.

      If text is drawn without a call to :meth:`.select_font_face`, (nor
      :meth:`.set_font_face` nor :meth:`.set_scaled_font`), the default family
      is platform-specific, but is essentially "sans-serif".  Default slant is
      cairo.FONT_SLANT_NORMAL, and default weight is
      cairo.FONT_WEIGHT_NORMAL.

      This function is equivalent to a call to :class:`ToyFontFace`
      followed by :meth:`.set_font_face`.

   .. method:: set_antialias(antialias)

      :param antialias: the new :ref:`ANTIALIAS <constants_ANTIALIAS>` mode

      Set the antialiasing mode of the rasterizer used for drawing shapes.
      This value is a hint, and a particular backend may or may not support a
      particular value.  At the current time, no backend supports
      :data:`cairo.ANTIALIAS_SUBPIXEL` when drawing shapes.

      Note that this option does not affect text rendering, instead see
      :meth:`FontOptions.set_antialias`.

   .. method:: set_dash(dashes, [offset=0])

      :param dashes: a sequence specifying alternate lengths of on and off
        stroke portions.
      :type dashes: sequence of float
      :param offset: an offset into the dash pattern at which the stroke
        should start, defaults to 0.
      :type offset: int
      :raises: :exc:`cairo.Error` if any value in *dashes* is negative, or if
        all values are 0.

      Sets the dash pattern to be used by :meth:`.stroke`. A dash pattern is
      specified by *dashes* - a sequence of positive values. Each value
      provides the length of alternate "on" and "off" portions of the
      stroke. The *offset* specifies an offset into the pattern at which the
      stroke begins.

      Each "on" segment will have caps applied as if the segment were a
      separate sub-path. In particular, it is valid to use an "on" length of
      0.0 with :data:`cairo.LINE_CAP_ROUND` or :data:`cairo.LINE_CAP_SQUARE`
      in order to distributed dots or squares along a path.

      Note: The length values are in user-space units as evaluated at the time
      of stroking. This is not necessarily the same as the user space at the
      time of :meth:`.set_dash`.

      If the number of dashes is 0 dashing is disabled.

      If the number of dashes is 1 a symmetric pattern is assumed with
      alternating on and off portions of the size specified by the single
      value in *dashes*.

   .. method:: set_fill_rule(fill_rule)

      :param fill_rule: 要设置的 :ref:`FILL RULE <constants_FILL_RULE>` 。填充规则用于
        决定一个区域是属于还是不属于一个复杂的路径（潜在的自相交等）。当前的填充规则会影响
        :meth:`.fill` 和 :meth:`.clip` 。

      默认的填充规则是 :data:`cairo.FILL_RULE_WINDING` 。

   .. method:: set_font_face(font_face)

      :param font_face: a :class:`FontFace`, or None to restore to the
        default :class:`FontFace`

      Replaces the current :class:`FontFace` object in the :class:`Context`
      with *font_face*.

   .. method:: set_font_matrix(matrix)

      :param matrix: a :class:`Matrix` describing a transform to be applied to
        the current font.

      Sets the current font matrix to *matrix*. The font matrix gives a
      transformation from the design space of the font (in this space, the
      em-square is 1 unit by 1 unit) to user space. Normally, a simple scale
      is used (see :meth:`.set_font_size`), but a more complex font matrix can
      be used to shear the font or stretch it unequally along the two axes

   .. method:: set_font_options(options)

      :param options: :class:`FontOptions` to use

      Sets a set of custom font rendering options for the :class:`Context`.
      Rendering options are derived by merging these options with the options
      derived from underlying surface; if the value in *options* has a default
      value (like :data:`cairo.ANTIALIAS_DEFAULT`), then the value from the
      surface is used.

   .. method:: set_font_size(size)

      :param size: the new font size, in user space units
      :type size: float

      Sets the current font matrix to a scale by a factor of *size*, replacing
      any font matrix previously set with :meth:`.set_font_size` or
      :meth:`.set_font_matrix`. This results in a font size of *size* user
      space units. (More precisely, this matrix will result in the font's
      em-square being a *size* by *size* square in user space.)

      If text is drawn without a call to :meth:`.set_font_size`, (nor
      :meth:`.set_font_matrix` nor :meth:`.set_scaled_font`), the default font
      size is 10.0.

   .. method:: set_line_cap(line_cap)

      :param line_cap: a :ref:`LINE_CAP <constants_LINE_CAP>` style

      Sets the current line cap style within the :class:`Context`.

      As with the other stroke parameters, the current line cap style is
      examined by :meth:`.stroke`, :meth:`.stroke_extents`, and
      :meth:`.stroke_to_path`, but does not have any effect during path
      construction.

      The default line cap style is :data:`cairo.LINE_CAP_BUTT`.

   .. method:: set_line_join(line_join)

      :param line_join: a :ref:`LINE_JOIN <constants_LINE_JOIN>` style

      Sets the current line join style within the :class:`Context`.

      As with the other stroke parameters, the current line join style is
      examined by :meth:`.stroke`, :meth:`.stroke_extents`, and
      :meth:`.stroke_to_path`, but does not have any effect during path
      construction.

      The default line join style is :data:`cairo.LINE_JOIN_MITER`.

   .. method:: set_line_width(width)

      :param width: a line width
      :type width: float

      Sets the current line width within the :class:`Context`. The line width
      value specifies the diameter of a pen that is circular in user space,
      (though device-space pen may be an ellipse in general due to
      scaling/shear/rotation of the CTM).

      Note: When the description above refers to user space and CTM it refers
      to the user space and CTM in effect at the time of the stroking
      operation, not the user space and CTM in effect at the time of the call
      to :meth:`.set_line_width`. The simplest usage makes both of these
      spaces identical. That is, if there is no change to the CTM between a
      call to :meth:`.set_line_width` and the stroking operation, then one can
      just pass user-space values to :meth:`.set_line_width` and ignore this
      note.

      As with the other stroke parameters, the current line width is examined
      by :meth:`.stroke`, :meth:`.stroke_extents`, and
      :meth:`.stroke_to_path`, but does not have any effect during path
      construction.

      The default line width value is 2.0.

   .. method:: set_matrix(matrix)

      :param matrix: a transformation :class:`Matrix` from user space to
        device space.

      Modifies the current transformation matrix (CTM) by setting it equal to
      *matrix*.

   .. method:: set_miter_limit(limit)

      :param limit: miter limit to set
      :type width: float

      Sets the current miter limit within the :class:`Context`.

      If the current line join style is set to :data:`cairo.LINE_JOIN_MITER`
      (see :meth:`.set_line_join`), the miter limit is used to determine
      whether the lines should be joined with a bevel instead of a miter.
      Cairo divides the length of the miter by the line width. If the result
      is greater than the miter limit, the style is converted to a bevel.

      As with the other stroke parameters, the current line miter limit is
      examined by :meth:`.stroke`, :meth:`.stroke_extents`, and
      :meth:`.stroke_to_path`, but does not have any effect during path
      construction.

      The default miter limit value is 10.0, which will convert joins with
      interior angles less than 11 degrees to bevels instead of miters. For
      reference, a miter limit of 2.0 makes the miter cutoff at 60 degrees,
      and a miter limit of 1.414 makes the cutoff at 90 degrees.

      A miter limit for a desired angle can be computed as::

        miter limit = 1/math.sin(angle/2)

   .. method:: set_operator(op)

      :param op: the compositing :ref:`OPERATOR <constants_OPERATOR>` to set
        for use in all drawing operations.

      The default operator is :data:`cairo.OPERATOR_OVER`.

   .. method:: set_scaled_font(scaled_font)

      :param scaled_font: a :class:`ScaledFont`

      Replaces the current font face, font matrix, and font options in the
      :class:`Context` with those of the :class:`ScaledFont`. Except for some
      translation, the current CTM of the :class:`Context` should be the same
      as that of the :class:`ScaledFont`, which can be accessed using
      :meth:`ScaledFont.get_ctm`.

      .. versionadded:: 1.2

   .. method:: set_source(source)

      :param source: a :class:`Pattern` to be used as the source for
        subsequent drawing operations.

      Sets the source pattern within :class:`Context` to *source*. This
      pattern will then be used for any subsequent drawing operation until a
      new source pattern is set.

      Note: The pattern's transformation matrix will be locked to the user
      space in effect at the time of :meth:`.set_source`. This means that
      further modifications of the current transformation matrix will not
      affect the source pattern. See :meth:`Pattern.set_matrix`.

      The default source pattern is a solid pattern that is opaque black,
      (that is, it is equivalent to ``set_source_rgb(0.0, 0.0, 0.0)``.

   .. method:: set_source_rgb(red, green, blue)

      :param red: red component of color
      :type red: float
      :param green: green component of color
      :type green: float
      :param blue: blue component of color
      :type blue: float

      Sets the source pattern within :class:`Context` to an opaque color. This
      opaque color will then be used for any subsequent drawing operation
      until a new source pattern is set.

      The color components are floating point numbers in the range 0 to
      1. If the values passed in are outside that range, they will be
      clamped.

      The default source pattern is opaque black, (that is, it is
      equivalent to ``set_source_rgb(0.0, 0.0, 0.0)``.

   .. method:: set_source_rgba(red, green, blue[, alpha=1.0])

      :param red: red component of color
      :type red: float
      :param green: green component of color
      :type green: float
      :param blue: blue component of color
      :type blue: float
      :param alpha: alpha component of color
      :type alpha: float

      Sets the source pattern within :class:`Context` to a translucent
      color. This color will then be used for any subsequent drawing operation
      until a new source pattern is set.

      The color and alpha components are floating point numbers in the range 0
      to 1. If the values passed in are outside that range, they will be
      clamped.

      The default source pattern is opaque black, (that is, it is
      equivalent to ``set_source_rgba(0.0, 0.0, 0.0, 1.0)``.

   .. method:: set_source_surface(surface[, x=0.0[, y=0.0]])

      :param surface: a :class:`Surface` to be used to set the source pattern
      :param x: User-space X coordinate for surface origin
      :type x: float
      :param y: User-space Y coordinate for surface origin
      :type y: float

      This is a convenience function for creating a pattern from a
      :class:`Surface` and setting it as the source in :class:`Context` with
      :meth:`.set_source`.

      The *x* and *y* parameters give the user-space coordinate at which the
      surface origin should appear. (The surface origin is its upper-left
      corner before any transformation has been applied.) The *x* and *y*
      patterns are negated and then set as translation values in the pattern
      matrix.

      Other than the initial translation pattern matrix, as described above,
      all other pattern attributes, (such as its extend mode), are set to the
      default values as in :class:`SurfacePattern`.  The resulting pattern can
      be queried with :meth:`.get_source` so that these attributes can be
      modified if desired, (eg. to create a repeating pattern with
      :meth:`.Pattern.set_extend`).

   .. method:: set_tolerance(tolerance)

      :param tolerance: the tolerance, in device units (typically pixels)
      :type tolerance: float

      Sets the tolerance used when converting paths into trapezoids.  Curved
      segments of the path will be subdivided until the maximum deviation
      between the original path and the polygonal approximation is less than
      *tolerance*. The default value is 0.1. A larger value will give better
      performance, a smaller value, better appearance. (Reducing the value
      from the default value of 0.1 is unlikely to improve appearance
      significantly.)  The accuracy of paths within Cairo is limited by the
      precision of its internal arithmetic, and the prescribed *tolerance* is
      restricted to the smallest representable internal value.

   .. method:: show_glyphs(glyphs[, num_glyphs])

      :param glyphs: glyphs to show
      :type glyphs: a sequence of (int, float, float)
      :param num_glyphs: number of glyphs to show, defaults to showing all
        glyphs
      :type num_glyphs: int

      A drawing operator that generates the shape from an array of glyphs,
      rendered according to the current font face, font size (font matrix),
      and font options.

   .. method:: show_page()

      Emits and clears the current page for backends that support multiple
      pages. Use :meth:`.copy_page` if you don't want to clear the page.

      This is a convenience function that simply calls
      ``ctx.get_target() . show_page()``

   .. method:: show_text(text)

      :param text: text
      :type text: str

      A drawing operator that generates the shape from a string of text,
      rendered according to the current font_face, font_size (font_matrix),
      and font_options.

      This function first computes a set of glyphs for the string of text. The
      first glyph is placed so that its origin is at the current point. The
      origin of each subsequent glyph is offset from that of the previous
      glyph by the advance values of the previous glyph.

      After this call the current point is moved to the origin of where the
      next glyph would be placed in this same progression. That is, the
      current point will be at the origin of the final glyph offset by its
      advance values. This allows for easy display of a single logical string
      with multiple calls to :meth:`.show_text`.

      Note: The :meth:`.show_text` function call is part of what the cairo
      designers call the "toy" text API. It is convenient for short demos
      and simple programs, but it is not expected to be adequate for
      serious text-using applications. See :meth:`.show_glyphs` for the
      "real" text display API in cairo.

   .. method:: stroke()

      A drawing operator that strokes the current path according to the
      current line width, line join, line cap, and dash settings. After
      :meth:`.stroke`, the current path will be cleared from the cairo
      context. See :meth:`.set_line_width`, :meth:`.set_line_join`,
      :meth:`.set_line_cap`, :meth:`.set_dash`, and :meth:`.stroke_preserve`.

      Note: Degenerate segments and sub-paths are treated specially and
      provide a useful result. These can result in two different situations:

      1. Zero-length "on" segments set in :meth:`.set_dash`. If the cap
      style is :data:`cairo.LINE_CAP_ROUND` or :data:`cairo.LINE_CAP_SQUARE`
      then these segments will be drawn as circular dots or squares
      respectively. In the case of :data:`cairo.LINE_CAP_SQUARE`, the
      orientation of the squares is determined by the direction of the
      underlying path.

      2. A sub-path created by :meth:`.move_to` followed by either a
      :meth:`.close_path` or one or more calls to :meth:`.line_to` to the same
      coordinate as the :meth:`.move_to`. If the cap style is
      :data:`cairo.LINE_CAP_ROUND` then these sub-paths will be drawn as
      circular dots. Note that in the case of :data:`cairo.LINE_CAP_SQUARE` a
      degenerate sub-path will not be drawn at all, (since the correct
      orientation is indeterminate).

      In no case will a cap style of :data:`cairo.LINE_CAP_BUTT` cause anything
      to be drawn in the case of either degenerate segments or sub-paths.

   .. method:: stroke_extents()

      :returns: (x1, y1, x2, y2)
      :rtype: (float, float, float, float)

      * *x1*: left of the resulting extents
      * *y1*: top of the resulting extents
      * *x2*: right of the resulting extents
      * *y2*: bottom of the resulting extents

      Computes a bounding box in user coordinates covering the area that would
      be affected, (the "inked" area), by a :meth:`.stroke` operation given
      the current path and stroke parameters. If the current path is empty,
      returns an empty rectangle (0, 0, 0, 0). Surface dimensions and
      clipping are not taken into account.

      Note that if the line width is set to exactly zero, then
      :meth:`.stroke_extents` will return an empty rectangle. Contrast with
      :meth:`.path_extents` which can be used to compute the non-empty bounds
      as the line width approaches zero.

      Note that :meth:`.stroke_extents` must necessarily do more work to
      compute the precise inked areas in light of the stroke parameters, so
      :meth:`.path_extents` may be more desirable for sake of performance if
      non-inked path extents are desired.

      See :meth:`.stroke`, :meth:`.set_line_width`, :meth:`.set_line_join`,
      :meth:`.set_line_cap`, :meth:`.set_dash`, and :meth:`.stroke_preserve`.

   .. method:: stroke_preserve()

      A drawing operator that strokes the current path according to the
      current line width, line join, line cap, and dash settings. Unlike
      :meth:`.stroke`, :meth:`.stroke_preserve` preserves the path within the
      cairo context.

      See :meth:`.set_line_width`, :meth:`.set_line_join`,
      :meth:`.set_line_cap`, :meth:`.set_dash`, and :meth:`.stroke_preserve`.

   .. method:: text_extents(text)

      :param text: text to get extents for
      :type text: str
      :returns: x_bearing, y_bearing, width, height, x_advance, y_advance
      :rtype: 6-tuple of float

      Gets the extents for a string of text. The extents describe a user-space
      rectangle that encloses the "inked" portion of the text, (as it would be
      drawn by :meth:`Context.show_text`). Additionally, the x_advance and
      y_advance values indicate the amount by which the current point would be
      advanced by :meth:`Context.show_text`.

      Note that whitespace characters do not directly contribute to the size
      of the rectangle (extents.width and extents.height). They do contribute
      indirectly by changing the position of non-whitespace characters. In
      particular, trailing whitespace characters are likely to not affect the
      size of the rectangle, though they will affect the x_advance and
      y_advance values.

   .. method:: text_path(text)

      :param text: text
      :type text: str

      Adds closed paths for text to the current path. The generated path if
      filled, achieves an effect similar to that of :meth:`Context.show_text`.

      Text conversion and positioning is done similar to
      :meth:`Context.show_text`.

      Like :meth:`Context.show_text`, After this call the current point is
      moved to the origin of where the next glyph would be placed in this same
      progression. That is, the current point will be at the origin of the
      final glyph offset by its advance values.  This allows for chaining
      multiple calls to to :meth:`Context.text_path` without having to set
      current point in between.

      Note: The :meth:`.text_path` function call is part of what the cairo
      designers call the "toy" text API. It is convenient for short demos and
      simple programs, but it is not expected to be adequate for serious
      text-using applications. See :meth:`Context.glyph_path` for the "real"
      text path API in cairo.

   .. method:: transform(matrix)

      :param matrix: a transformation :class:`Matrix` to be applied to the
        user-space axes

      Modifies the current transformation matrix (CTM) by applying *matrix* as
      an additional transformation. The new transformation of user space takes
      place after any existing transformation.

   .. method:: translate(tx, ty)

      :param tx: amount to translate in the X direction
      :type tx: float
      :param ty: amount to translate in the Y direction
      :type ty: float

      Modifies the current transformation matrix (CTM) by translating the
      user-space origin by *(tx, ty)*. This offset is interpreted as a
      user-space coordinate according to the CTM in place before the new call
      to :meth:`.translate`. In other words, the translation of the user-space
      origin takes place after any existing transformation.

   .. method:: user_to_device(x, y)

      :param x: X value of coordinate
      :type x: float
      :param y: Y value of coordinate
      :type y: float
      :returns: (x, y)
      :rtype: (float, float)

      * *x*: X value of coordinate
      * *y*: Y value of coordinate

      Transform a coordinate from user space to device space by multiplying
      the given point by the current transformation matrix (CTM).

   .. method:: user_to_device_distance(dx, dy)

      :param dx: X value of a distance vector
      :type dx: float
      :param dy: Y value of a distance vector
      :type dy: float
      :returns: (dx, dy)
      :rtype: (float, float)

      * *dx*: X value of a distance vector
      * *dy*: Y value of a distance vector

      Transform a distance vector from user space to device space. This
      function is similar to :meth:`Context.user_to_device` except that the
      translation components of the CTM will be ignored when transforming
      *(dx,dy)*.
