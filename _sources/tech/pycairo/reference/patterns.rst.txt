.. _patterns:

********
Pattern
********

.. currentmodule:: cairo


Pattern是cairo绘图的颜料，其主要应用时作为所有cairo绘制操作的源，当然也可以用于mask，即画笔。

一个cairo *Pattern* 由以下列出的任何一个 *PatternType* 的构造函数来创建，或者可以隐式的通过
*Context.set_source_<type>()* 方法来创建。


class Pattern()
===============

*Pattern* 是所有其他pattern类继承的抽象基类，不能直接被实例化。

.. class:: Pattern()

   .. method:: get_extend()

      :returns: 绘制 *Pattern* 时当前的扩展模式（ :ref:`EXTEND 属性 <constants_EXTEND>` ）。
      :rtype: int

      获取 *Pattern* 当前的扩展模式。每种扩展模式的详细信息参考 :ref:`EXTEND 属性 <constants_EXTEND>` 。

   .. method:: get_matrix()

      :returns: 存储了 *Pattern* 的仿射变换矩阵信息的类 :class:`Matrix` 。

   .. method:: set_extend(extend)

      :param extend: 描述 *Pattern* 外围区域如何绘制的 :ref:`EXTEND <constants_EXTEND>` 。

      设置绘制 *Pattern* 外围区域时使用的模式。

      对于 :class:`SurfacePattern` 和 :data:`cairo.EXTEND_PAD` 默认的模式是 :data:`cairo.EXTEND_NONE` 。
      对于 :class:`Gradient` Pattern 默认的模式时 :data:`cairo.EXTEND_PAD` 。

   .. method:: set_matrix(matrix)

      :param matrix: :class:`Matrix` 的实例

      设置 *Pattern* 的变换矩阵为 *matrix* 。这个矩阵用于从用户空间转换到pattern空间。

      当 *Patter* 第一次被创建时总是会创建一个唯一的变换矩阵用于其仿射变换，因此
      pattern空间和用户空间从一开始就是不同的。

      重要: 请注意这个变化矩阵的方向是从用户空间到pattern空间，这意味着如果你想要从
      pattern空间到用户空间（即设备空间），那么其坐标变换使用的是 *Pattern* 矩阵的反转矩阵。

      例如，如果你想要创建一个比之前大一倍的 *Pattern* ，正确的代码应该是::

        matrix = cairo.Matrix(xx=0.5,yy=0.5)
        pattern.set_matrix(matrix)

      如果在上面的代码中使用值2.0代替0.5，会使得 *Patter* 是原来大小的一半。

      另外，需要注意的时用户空间的讨论仅限于 :class:`Context.set_source` 语义范围内。


class SolidPattern(:class:`Pattern`)
====================================

.. class:: SolidPattern(red, green, blue, alpha=1.0)

   :param red: 颜色的红色组件的值
   :type red: float
   :param green: 颜色的绿色组件的值
   :type green: float
   :param blue: 颜色的蓝色组件的值
   :type blue: float
   :param alpha: 颜色的alpha组件的值
   :type alpha: float
   :returns: 一个新的 *SolidPattern* 的实例
   :raises: 没有内存时触发 *MemoryError* 异常

   使用参数中的半透明颜色创建一个新的 *SolidPattern* 。颜色组件为0~1的浮点数。
   如果传递的参数超过这个范围，则使用最接近该值的范围内的值（clamped）。


   .. method:: get_rgba()

      :returns: (red, green, blue, alpha) 浮点数元组

      获取 *SolidPattern* 的颜色。

      .. versionadded:: 1.4


class SurfacePattern(:class:`Pattern`)
======================================

.. class:: SurfacePattern(surface)

   :param surface: cairo :class:`Surface`
   :returns: 使用参数surface新创建的 *SurfacePattern*
   :raises: 没有内存时触发 *MemoryError* 异常

   .. method:: get_filter()

      :returns: 当前用于调整 *SurfacePattern* 的 :ref:`FILTER <constants_filter>` 。

   .. method:: get_surface()

      :returns: *SurfacePattern* 的 :class:`Surface` 

      .. versionadded:: 1.4

   .. method:: set_filter(filter)

      :param filter: 用于描述如何调整 *Pattern* 的 :ref:`FILTER <constants_filter>` 。

      注意：即使你并没有使用 *Pattern* 时（例如使用 :meth:`Context.set_source_surface` 时）也想要控制调整的模式。
      这种情况下使用 :meth:`Context.get_source` 来访问 cairo 隐式创建的 pattern 更方便。
      例如::

        context.set_source_surface(image, x, y)
        surfacepattern.set_filter(context.get_source(), cairo.FILTER_NEAREST)


class Gradient(:class:`Pattern`)
================================

*Pattern* 是其他pattern类继承的抽象基类，不能直接被实例化。

.. class:: Gradient()

   .. method:: add_color_stop_rgb(offset, red, green, blue)

      :param offset: [0.0 .. 1.0] 范围内的偏移值
      :type offset: float
      :param red: 颜色的红色组件的值
      :type red: float
      :param green: 颜色的绿色组件的值
      :type green: float
      :param blue: 颜色的蓝色组件的值
      :type blue: float

      向 *Gradient* 添加一个不透明的颜色。
      offset 为沿着渐变的控制向量的位置点。例如，线性渐变 *LinearGradient's* 的控制向量
      从 (x0,y0) 到 (x1,y1) ，而径向渐变 *RadialGradient's* 的控制向量从圆的起点到圆的终点。

      颜色设置方法与 :meth:`Context.set_source_rgb` 相同。

      如果设置了两个（或更多个）点，则所有的停止点会根据添加顺序排序（添加早的点在前）。
      这在想要创建尖锐的颜色渐变（sharp color transition）而非混合（blend）渐变时很有用。

   .. method:: add_color_stop_rgba(offset, red, green, blue, alpha)

      :param offset: [0.0 .. 1.0] 范围内的偏移值
      :type offset: float
      :param red: 颜色的红色组件的值
      :type red: float
      :param green: 颜色的绿色组件的值
      :type green: float
      :param blue: 颜色的蓝色组件的值
      :type blue: float
      :param alpha: 颜色的alpha组件的值

      向 *Gradient* 添加一个不透明的颜色。 （译注：原文如此，疑有误）
      offset 为沿着渐变的控制向量的位置点。例如，线性渐变 *LinearGradient's* 的控制向量
      从 (x0,y0) 到 (x1,y1) ，而径向渐变 *RadialGradient's* 的控制向量从圆的起点到圆的终点。

      颜色设置方法与 :meth:`Context.set_source_rgb` 相同。

      如果设置了两个（或更多个）点，则所有的停止点会根据添加顺序排序（添加早的点在前）。
      这在想要创建尖锐的颜色渐变（sharp color transition）而非混合（blend）渐变时很有用。


class LinearGradient(:class:`Gradient`)
=======================================
.. class:: LinearGradient(x0, y0, x1, y1)

   :param x0: 起始点的x坐标
   :type x0: float
   :param y0: 起始点的y坐标
   :type y0: float
   :param x1: 结束点的x坐标
   :type x1: float
   :param y1: 结束点的y坐标
   :type y1: float
   :returns: *LinearGradient*
   :raises: 没有内存时触发 *MemoryError* 异常

   根据 (x0, y0) 和 (x1,y1) 确定的直线创建一个新的 *LinearGradient* 。
   在使用 *Gradient* pattern之前，需要使用 :meth:`Gradient.add_color_stop_rgb` 
   或者 :meth:`Gradient.add_color_stop_rgba` 定义一系列的停止点。

   注意: 此处的坐标为pattern空间。对于一个新的 *Pattern* ，pattern空间与用户空间时不同的，
   但是他们之间的关系可以通过 :meth:`Pattern.set_matrix` 改变。

   .. method:: get_linear_points()

      :returns: (x0, y0, x1, y1) - 浮点数元组

        * x0: 第一个点的x坐标
        * y0: 第一个点的y坐标
        * x1: 第二个点的x坐标
        * y1: 第二个点的y坐标

      获取 *LinearGradient* 渐变的端点坐标。

      .. versionadded:: 1.4


class RadialGradient(:class:`Gradient`)
=======================================
.. class:: RadialGradient(cx0, cy0, radius0, cx1, cy1, radius1)

   :param cx0: 起始圆心的x坐标
   :type cx0: float
   :param cy0: 起始圆心的y坐标
   :type cy0: float
   :param radius0: 起始圆的半径
   :type radius0: float
   :param cx1: 终点圆心的x坐标
   :type cx1: float
   :param cy1: 终点圆心的y坐标
   :type cy1: float
   :param radius1: 终点圆的半径
   :type radius1: float
   :returns: 新创建的 *RadialGradient*
   :raises: 没有内存时触发 *MemoryError* 异常

   在(cx0, cy0, radius0) 和 (cx1, cy1, radius1) 两个圆之间创建一个新的 *RadialGradient* 径向渐变pattern。
   在使用 *Gradient* pattern之前，需要使用 :meth:`Gradient.add_color_stop_rgb` 
   或者 :meth:`Gradient.add_color_stop_rgba` 定义一系列的停止点。

   注意: 此处的坐标为pattern空间。对于一个新的 *Pattern* ，pattern空间与用户空间时不同的，
   但是他们之间的关系可以通过 :meth:`Pattern.set_matrix` 改变。

   .. method:: get_radial_circles()

      :returns: (x0, y0, r0, x1, y1, r1) - 一个浮点数元组

	* x0: 起始圆心的x坐标
	* y0: 起始圆心的y坐标
	* r0: 起始圆的半径
	* x1: 终点圆心的x坐标
	* y1: 终点圆心的y坐标
	* r1: 终点圆的半径

      获取 *RadialGradient* 的端点的圆，每个圆以其圆心坐标和半径表示。

      .. versionadded:: 1.4