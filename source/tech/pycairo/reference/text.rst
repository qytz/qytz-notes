.. _text:

****
Text
****

.. currentmodule:: cairo

cairo有两种方式可以解析字体：

* 一种是cairo的'玩具'text API。这个玩具API使用UTF-8编码的文本并且其功能仅限制为
  解析从左到右的文本，没有高级特性。这意味着像Hebrew，Arabic和Indic字体
  这些最复杂的字体（script）并不在讨论范围内，也没有字符间距调整或字体位置相关的标记。
  字体的选择也很受限制，同时也不能处理选择的字体并不包含要显示的文本的问题。
  这个API起始真的就是一个玩具，用于测试和演示的目的，任何认真考虑的程序都应该避免使用该API。

* 另一种使用cairo底层text API的方式可以访问字形的名字。底层的API需要用户将文本转换为字形
  索引和位置。这其实是一件很麻烦的事最好使用外部库来处理，比如pangocairo，Pango文本布局和解析库的一部分。
  Pango的网站 http://www.pango.org/



class FontFace()
================

*cairo.FontFace* 定义了字体除字体大小和字体矩阵
（字体矩阵用于改变字体，在不同方向不同的切向或缩放字体）外的所有方面。
:class:`Context` 可以通过:meth:`Context.set_font_face` 设置 *FontFace* ，字体
大小和矩阵可以通过 :meth:`Context.set_font_size` 和 :meth:`Context.set_font_matrix` 来设置。

根据使用的字体后端，有多种 *FontFace* 。

.. class:: FontFace()

   .. note:: 这个类不能被直接实例化，是由 :meth:`Context.get_font_face` 返回的。



class FreeTypeFontFace(:class:`FontFace`)
=========================================

FreeType Fonts - 支持FreeType的字体

FreeType字体后端主要用于GNU/Linux 上的字体渲染，也可以用于其他平台。

   .. note:: FreeType 字体在pycairo中没有实现，因为目前并没有提供C API的FreeType（和fontconfig）的开源python绑定，如果有人有兴趣为pycairo添加FreeType支持也可以。


class ToyFontFace(:class:`FontFace`)
====================================

*cairo.ToyFontFace* 相比与 :meth:`Context.select_font_face` 可以创建一个独立于context的toy font 。
class can be used instead of :meth:`Context.select_font_face` to create a toy font independently of a context.

.. class:: ToyFontFace(family[, slant[, weight]])

   :param family: font family名
   :type family: str
   :param slant: 字体的 :ref:`FONT_SLANT <constants_FONT_SLANT>` 属性，
     defaults to :data:`cairo.FONT_SLANT_NORMAL`.
   :param weight: 字体的 :ref:`FONT_WEIGHT <constants_FONT_WEIGHT>` 属性，
     defaults to :data:`cairo.FONT_WEIGHT_NORMAL`.
   :returns: 一个新的 *ToyFontFace*

   根据family、slant、weight三元组创建一个 *ToyFontFace* 。这些font face用于实现'toy' API。

   如果family 为0长字符串 ""，则使用平台特定的默认family。默认的family可以使用 :meth:`.get_family` 来查询。

   :meth:`Context.select_font_face` 使用此接口来创建font face，参考该函数以了解toy font face的限制。

   .. versionadded:: 1.8.4

   .. method:: get_family()

      :returns: toy font的family
      :rtype: str

      .. versionadded:: 1.8.4

   .. method:: get_slant()

      :returns: :ref:`FONT_SLANT <constants_FONT_SLANT>` 的值

      .. versionadded:: 1.8.4

   .. method:: get_weight()

      :returns: :ref:`FONT_WEIGHT <constants_FONT_WEIGHT>` 的值

      .. versionadded:: 1.8.4


class UserFontFace(:class:`FontFace`)
=====================================

user-font 特性允许cairo用户提供字体字形的绘制。这在实现非标准格式的字体时很有用，比如
SVG字体和Flash字体，但是也可以用于游戏和其他程序来绘制“有意思”的字体。

   .. note:: UserFontFace  支持还没有添加到pcairo中。如果你需要在pycairo中使用这个特性，请
      向cairo的邮件列表发送消息或者向pycairo报告bug。


class ScaledFont()
==================

*ScaledFont* 是一个缩放到特定尺寸和设备解析度的字体，其在使用底层字体很有用，例如
库或应用想要缓存缩放字体的引用来加速计算。

根据使用的字体后端，有多种缩放字体。

.. class:: ScaledFont(font_face, font_matrix, ctm, options)

   :param font_face: :class:`FontFace` 的实例
   :param font_matrix: 字体的字体空间到用户空间转换的矩阵 :class:`Matrix` 。对于最简单的情况，一个N个点的字体，矩阵
     只是缩放N，但是矩阵也可以用于在不同的轴有不同的缩放以拉伸或改变字体的形状，参考 :meth:`Context.set_font_matrix` 。
   :param ctm: 字体使用的用户空间到设备空间转换的矩阵 :class:`Matrix` 。
   :param options: :class:`FontOptions` 实例，用于获取或解析字体。

   根据 *FontFace* 和描述字体尺寸及使用环境的矩阵创建一个 *ScaledFont* 对象。

   .. method:: extents()

      :returns: (ascent, descent, height, max_x_advance, max_y_advance)，一个浮点数元组

      获取 *ScaledFont* 的metric信息。

   .. method:: get_ctm()

      pycairo中暂未实现。

   .. method:: get_font_face()

      :returns: 使用 *ScaledFont* 的 :class:`FontFace` 。

      .. versionadded:: 1.2

   .. method:: get_font_matrix()

      pycairo中暂未实现。

   .. method:: get_font_options()

      pycairo中暂未实现。

   .. method:: get_scale_matrix()

      :returns: 缩放矩阵 :class:`Matrix`

      缩放矩阵是字体矩阵和与字体关联的当前转换矩阵ctm的产物，即是从字体空间到设备空间的映射。

      .. versionadded:: 1.8


   .. method:: glyph_extents()

      pycairo中暂未实现。


   .. method:: text_extents(text)

      :param text: text
      :type text: str
      :returns: (x_bearing, y_bearing, width, height, x_advance, y_advance)
      :rtype: 六个浮点数的元组

      获取文本字符串的范围（extent），该范围使用一个包含文本绘制的范围的用户空间的矩形描述。
      该范围从原点（0,0）开始，因为如果cairo的状态被设置为相同的font face，font matrix，ctm和
      字体选项 *ScaledFont* ，其将要用 :meth:`Context.show_text` 来绘制。
      另外，x_advance和y_advance的值表示当前点会被 :meth:`Context.show_text` 推进的值。

      as it would be drawn by :meth:`Context.show_text` if the
      cairo graphics state were set to the same font_face, font_matrix, ctm,
      and font_options as *ScaledFont* .
      Additionally, the x_advance and y_advance values indicate the amount by which the current point would be
      advanced by :meth:`Context.show_text`.

      注意空白字符并未直接体现在矩形的尺寸（宽和高）上，这些字符间接的改变了非空白字符的位置。
      尤其是尾部的空白字符很可能不会影响该矩形的尺寸，尽管他们会印象 x_advance 和 y_advance 的值。

      .. versionadded:: 1.2

   .. method:: text_to_glyphs()

      pycairo中暂未实现。



class FontOptions()
===================

一个“不透明”的结构，存储了渲染字体时用到的所有选项。

*FontOptions* 的每个特性可以通过函数 *FontOptions.set_<feature_name>* 或 *FontOptions.get_<feature_name>* 被设置或访问，
例如 :meth:`FontOptions.set_antialias` 和 :meth:`FontOptions.get_antialias` 。

未来可能会为 *FontOptions* 添加新的特性，因此应该使用 :meth:`FontOptions.copy()` 、 :meth:`FontOptions.equal()` 、
:meth:`FontOptions.merge()` 和 :meth:`FontOptions.hash()` 执行拷贝、检查相等、合并或计算FontOptions hash值的操作。

.. class:: FontOptions()

   :returns: 一个新分配的 *FontOptions*.

   分配一个新的 *FontOptions* 对象，所有的选项被初始化为默认值。

   .. method:: get_antialias()

      :returns: *FontOptions* 对象的 :ref:`ANTIALIAS <constants_ANTIALIAS>` 模式。

   .. method:: get_hint_metrics()

      :returns: *FontOptions* 对象的 :ref:`HINT METRICS <constants_HINT_METRICS>` 模式。

   .. method:: get_hint_style()

      :returns: *FontOptions* 对象的 :ref:`HINT STYLE <constants_HINT_STYLE>` 。

   .. method:: get_subpixel_order()

      :returns: *FontOptions* 对象的 :ref:`SUBPIXEL_ORDER <constants_SUBPIXEL_ORDER>` 。

   .. method:: set_antialias(antialias)

      :param antialias: :ref:`ANTIALIAS <constants_ANTIALIAS>` 模式。

      这个选项设置了渲染字体时抗锯齿的类型。

   .. method:: set_hint_metrics(hint_metrics)

      :param hint_metrics: :ref:`HINT METRICS <constants_HINT_METRICS>` 模式。

      这个选项控制 metrics 在设备单元是否被量化为整数。

   .. method:: set_hint_style(hint_style)

      :param hint_style: :ref:`HINT STYLE <constants_HINT_STYLE>`

      这个选项控制是否使字体轮廓适配像素网格，如果是，时优化字体显示更忠实于原字体或者使用更高的对比度。

   .. method:: set_subpixel_order(subpixel_order)

      :param subpixel_order: :ref:`SUBPIXEL_ORDER <constants_SUBPIXEL_ORDER>`

      亚像素顺序描述使用亚像素抗锯齿模式 :data:`cairo.ANTIALIAS_SUBPIXEL` 渲染时显示设备中每个像素中原色颜色的顺序。
