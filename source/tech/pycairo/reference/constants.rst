.. _constants:

******************************
模块函数与常量
******************************

.. currentmodule:: cairo


模块函数
================

.. function:: cairo_version()

   :returns: 编码后的版本号
   :rtype: int

   返回编码为一个整数的底层cairo C库的版本号。

.. function:: cairo_version_string()

   :returns: 编码后的版本号
   :rtype: str

   以便于人类阅读的"X.Y.Z"字符串形式返回底层cairo C库的版本号。


模块常量
================

.. data:: version

   pycairo的版本，字符串类型。

.. data:: version_info

   pycairo的版本号，元组类型。


.. _constants_HAS:

cairo.HAS
---------
.. data:: HAS_ATSUI_FONT
          HAS_FT_FONT
          HAS_GLITZ_SURFACE
          HAS_IMAGE_SURFACE
          HAS_PDF_SURFACE
          HAS_PNG_FUNCTIONS
          HAS_PS_SURFACE
          HAS_SVG_SURFACE
          HAS_USER_FONT
          HAS_QUARTZ_SURFACE
          HAS_WIN32_FONT
          HAS_WIN32_SURFACE
          HAS_XCB_SURFACE
          HAS_XLIB_SURFACE

   1 代表底层cairo C库支持该特性，0 代表不支持。


.. _constants_ANTIALIAS:

cairo.ANTIALIAS
---------------
ANTIALIAS 指定了渲染文本或形状时的抗锯齿类型。

.. data:: ANTIALIAS_DEFAULT

   针对子系统和目标设备使用默认的抗锯齿。

.. data:: ANTIALIAS_NONE

   使用双级Alpha遮罩(bilevel alpha mask)。

.. data:: ANTIALIAS_GRAY

   使用单色抗锯齿（例如使用白色背景上黑色文本的灰度）。

.. data:: ANTIALIAS_SUBPIXEL

  通过利用LCD面板等设备的亚像素渲染特性实现抗锯齿效果。
  （译注：相关内容可以参考  `亚像素显示 <http://www.xieyidian.com/105a7>`_ ）


.. _constants_CONTENT:

cairo.CONTENT
-------------
这些常量用于描述 :class:`Surface` 包含的内容，即颜色信息、alpha信息（半透明vs不透明度），或者两者都有。

.. data:: CONTENT_COLOR

   surface 只包含颜色信息。

.. data:: CONTENT_ALPHA

   surface 只包含alpha通道信息。

.. data:: CONTENT_COLOR_ALPHA

   surface 包含颜色和alpha信息。


.. _constants_EXTEND:

cairo.EXTEND
------------
这些常量用来描述 :class:`Pattern` 对于超出pattern正常区域的颜色/alpha如何渲染的问题，
（例如：超出surface边界或者超出渐变区域边界）。

对于  :class:`SurfacePattern` 默认的模式是 *EXTEND_NONE* ，对于 :class:`Gradient` 的pattern，
默认的模式是 *EXTEND_PAD* 。

.. data:: EXTEND_NONE

   超过source pattern边界的像素完全透明。

.. data:: EXTEND_REPEAT

   （超出部分）pattern被重复的平铺。

.. data:: EXTEND_REFLECT

   pattern通过反射边缘平铺（>=1.6版本实现）。
   the pattern is tiled by reflecting at the edges (Implemented for surface
   patterns since 1.6)

.. data:: EXTEND_PAD

   超出pattern边界部分的像素直接拷贝与其相邻的边界部分的像素（>=1.2版本，只有>=1.6版本的surface pattern实现）。

未来的版本可能会增加新的模式。


.. _constants_FILL_RULE:

cairo.FILL_RULE
---------------
这些常量用于选择path填充的模式。对于所有这两种模式，一个点是否被填充取决于：
从该点向无穷远画一条射线，该射线与path的交叉点。射线的方向任意，只要交叉点不通过path某一段的终点，
或者与path相切（事实上填充并不是按照这种方式实现的，这只是填充规则的描述）。

默认的填充规则是 *FILL_RULE_WINDING* 。

.. data:: FILL_RULE_WINDING

   如果路径从左向右穿过射线，count+1，如果路径从右向左穿过射线，count-1。
   （左和右由射线的起点看起），如果count最终非0，该点被填充。

   If the path crosses the ray from left-to-right, counts +1. If the path
   crosses the ray from right to left, counts -1. (Left and right are
   determined from the perspective of looking along the ray from the starting
   point.) If the total count is non-zero, the point will be filled.

.. data::  FILL_RULE_EVEN_ODD

   不考虑方向，统计交叉点的总数，如果总数是奇数，则该点被填充。


未来的版本可能会增加新的模式。


.. _constants_FILTER:

cairo.FILTER
------------
这些常量用于描述渲染pattern的像素点时使用的filter。
函数 :meth:`SurfacePattern.set_filter` 可以设置pattern要使用的filter。

.. data:: FILTER_FAST

   一个高性能的filter，质量与 *FILTER_NEAREST* 差不多。

.. data:: FILTER_GOOD

   性能一般的filter，质量与 *FILTER_BILINEAR* 差不多。

.. data:: FILTER_BEST

   最高质量的可用的filter，性能可能并不适合交互界面使用。

.. data:: FILTER_NEAREST

   近邻过滤（Nearest-neighbor filtering）。

.. data:: FILTER_BILINEAR

   二维线性差值（Linear interpolation in two dimensions）。

.. data:: FILTER_GAUSSIAN

   该值当前未实现，当前代码不应该使用。


.. _constants_FONT_SLANT:

cairo.FONT_SLANT
----------------
这些常量用于描述 :class:`FontFace` 的倾斜度。

.. data:: FONT_SLANT_NORMAL

   正常的字体风格。

.. data:: FONT_SLANT_ITALIC

   斜体风格（Italic font style）。

.. data:: FONT_SLANT_OBLIQUE

   伪斜体风格（Oblique font style）。

   译注：参考 `伪斜体 <http://zh.wikipedia.org/wiki/%E4%BC%AA%E6%96%9C%E4%BD%93>`_


.. _constants_FONT_WEIGHT:

cairo.FONT_WEIGHT
-----------------
这些常量描述了 :class:`FontFace` 的字体的粗细。

.. data:: FONT_WEIGHT_NORMAL

   正常的自体粗细形式。

.. data:: FONT_WEIGHT_BOLD

   粗体形式。


.. _constants_FORMAT:

cairo.FORMAT
------------
这些常量描述:class:`ImageSurface` 数据在内存中的格式。

未来的版本可能会增加新的格式。

.. data:: FORMAT_ARGB32

   每个像素32位，高8位描述alpha通道，然后是红、绿、蓝三原色。该32位的值以本地字节序存储。
   最终的渲染会使用预乘过的alpha值（即红色50%透明的值是0x80800000，而不是0x80ff0000）。

.. data:: FORMAT_RGB24

   每个像素点是一个32位的值，但高8位没有使用，红、绿、蓝三原色依序存储在余下的24位中。

.. data:: FORMAT_A8

   每个像素点8位——存储alpha通道的值。

.. data:: FORMAT_A1

   每个像素使用1位，用于存储alpha值。很多像素点一起打包成32位的数，位序按照平台序来定。在大端机器上，
   第一个像素在最高位，在小端机器上第一个像素在最低位。

.. data:: FORMAT_RGB16_565

   每个像素16位，其中依序红色在高5位，绿色在中间6位，蓝色在低5位。


.. _constants_HINT_METRICS:

cairo.HINT_METRICS
------------------
这些常量描述是否微调字体规格（hint font metrics），意即量化字体规格，字体在显示设备空间的表示为整数。这样做可以
提高字母和线段间距的连续性，但是也意味着文字在不同的缩放程度时的布局可能会不同。

.. data:: HINT_METRICS_DEFAULT

   以字体后端和目标设备默认的方式微调字体。

.. data:: HINT_METRICS_OFF

   不微调字体规格。

.. data:: HINT_METRICS_ON

   微调字体规格。


.. _constants_HINT_STYLE:

cairo.HINT_STYLE
----------------
这些常量描述对字体轮廓微调的类型。微调的主要工作是将字体的轮廓过滤映射到像素栅格以提升外观。
由于微调后的轮廓可能会与原来的稍有不同，因此渲染出来的字体可能并不完全忠实于原来的外形轮廓。
并不是所有的微调类型被所有字体后端支持。

.. data:: HINT_STYLE_DEFAULT

   使用字体后端及目标设备的默认类型。

.. data:: HINT_STYLE_NONE

   不微调字体廓量。

.. data:: HINT_STYLE_SLIGHT

   轻微的调整来提高对比度，尽量忠实与原始形状。

.. data:: HINT_STYLE_MEDIUM

   中度的调整在忠实于原始形状与对比度之间尽量折衷。

.. data:: HINT_STYLE_FULL

   调整轮廓以获取尽可能大的对比度。

为了版本可能会增加新的类型。


.. _constants_LINE_CAP:

cairo.LINE_CAP
--------------
这些常量描述在一次绘画(stroke)时如何处理路径的端点。

默认的形式是 *LINE_CAP_BUTT*

.. data:: LINE_CAP_BUTT

   在开始（结束）点停止线段。

.. data:: LINE_CAP_ROUND

   在端点增加圆角，圆心就是线段的端点。

.. data:: LINE_CAP_SQUARE

   在端点增加一个正方形，正方形的中心在线段的端点。


.. _constants_LINE_JOIN:

cairo.LINE_JOIN
---------------
这些常量描述当完成一次绘画时如何渲染两条线段的交叉点。

默认的样式是 *LINE_JOIN_MITER*

.. data:: LINE_JOIN_MITER

   圆角的交叉点，参考： :meth:`Context.set_miter_limit`

.. data:: LINE_JOIN_ROUND

   圆角的交叉点，圆心正是交叉点。

.. data:: LINE_JOIN_BEVEL

   斜角的交叉点，在一半线宽的位置切掉交叉点的尖角。


.. _constants_OPERATOR:

cairo.OPERATOR
--------------
这些常量用于设置cairo绘画操作的合成操作。

默认的操作符是 *OPERATOR_OVER*.

标记为 *unbounded* 的操作符即使超出了屏蔽层（mask layer）也会修改，即屏蔽层并不能限制这些效果的范围。
但是通过clip这样的方式仍然能限制有效的范围。

为了使事情变的简单，此处只记录了这些操作符在源和目的或者都透明或者都不透明时的行为，
其实实现对半透明效果也支持。

要获取每个操作符更加详细的信息，包括其数学原理，请参考： http://cairographics.org/operators.

.. data:: OPERATOR_CLEAR

   完全清除目的层 (bounded)

.. data:: OPERATOR_SOURCE

   完全替换目的层(bounded)

.. data:: OPERATOR_OVER

   在目的层的上面绘制源的内容(bounded)

.. data:: OPERATOR_IN

   在目的层有内容的地方绘制源。(unbounded)

.. data:: OPERATOR_OUT

   在目的层没有内容的地方绘制源。(unbounded)

.. data:: OPERATOR_ATOP

   只在目的层内容的上面绘制源。

.. data:: OPERATOR_DEST

   忽略源。

.. data:: OPERATOR_DEST_OVER

   在源上面绘制目的层。

.. data:: OPERATOR_DEST_IN

   只在源有内容的地方保留目的层。(unbounded)

.. data:: OPERATOR_DEST_OUT

   只在源没有内容的地方保留目的层。

.. data:: OPERATOR_DEST_ATOP

   只保留源有内容的地方的目的层内容。(unbounded)

.. data:: OPERATOR_XOR

   源和目的执行异或操作（只有源或者目的时绘制）。

.. data:: OPERATOR_ADD

   源和目的层累积。

.. data:: OPERATOR_SATURATE

   与OPERATOR_OVER类似，但是假定源和目的几何上分离（but assuming source and dest are disjoint geometries）。


.. _constants_PATH:

cairo.PATH
----------
这些常量描述 :class:`Path` 的类型。

These constants are used to describe the type of one portion of a path when
represented as a :class:`Path`.

.. 详情参见： #cairo_path_data_t 

.. data:: PATH_MOVE_TO

   move-to 操作

.. data:: PATH_LINE_TO

   line-to 操作

.. data:: PATH_CURVE_TO

   curve-to 操作

.. data:: PATH_CLOSE_PATH

   close-path 操作


.. _constants_PS_LEVEL:

cairo.PS_LEVEL
--------------
这些常量描述生成的PostScript文件的版本。注意：只有cairo编译时开启了PS支持时才会定义这些常量。

.. data:: PS_LEVEL_2

   PostScript level 2

.. data:: PS_LEVEL_3

   PostScript level 3


.. _constants_SUBPIXEL_ORDER:

cairo.SUBPIXEL_ORDER
--------------------
亚像素顺序（The subpixel order）描述了在显示设备上开启抗锯齿模式 :data:`ANTIALIAS_SUBPIXEL` 时
每个像素点色彩元素的顺序。

.. data:: SUBPIXEL_ORDER_DEFAULT

   使用目的显示设备默认的亚像素顺序。

.. data:: SUBPIXEL_ORDER_RGB

   亚像素按照红色在做的顺序水平排列。

.. data:: SUBPIXEL_ORDER_BGR

   亚像素按照蓝像素在做的顺序水平排列。

.. data:: SUBPIXEL_ORDER_VRGB

   亚像素按照红色在顶的顺序竖直排列。

.. data:: SUBPIXEL_ORDER_VBGR

   亚像素按照蓝色在顶的顺序竖直排列。

