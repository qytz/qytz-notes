.. _matrix:

******
Matrix
******

.. currentmodule:: cairo


class Matrix()
==============

*Matrix* 在cairo中被广泛的用于不同坐标系统间的转换。一个 *Matrix* 代表一个仿射变换，例如
缩放、旋转、剪辑（shear）或以上几种的组合。点 (x, y) 的转换通过如下方式给出::

  x_new = xx * x + xy * y + x0
  y_new = yx * x + yy * y + y0

:class:`Context` 的当前转换矩阵CTX即 *Matrix* ，定义了从用户空间坐标到设备空间坐标的转换。

一些标准的Python操作可以被用于矩阵 matrix:

读取矩阵 *Matrix* 的值::

  xx, yx, xy, yy, x0, y0 = matrix

两个矩阵相乘::

  matrix3 = matrix1.multiply(matrix2)
  # or equivalently
  matrix3 = matrix1 * matrix2

比较两个矩阵::

  matrix1 == matrix2
  matrix1 != matrix2

更多矩阵转换相关的内容请参考 http://www.cairographics.org/matrix_transform
（译注，矩阵相关的文章 http://blog.csdn.net/xiaojidan2011/article/details/8213873 ）


.. class:: Matrix(xx = 1.0, yx = 0.0, xy = 0.0, yy = 1.0, x0 = 0.0, y0 = 0.0)

   :param xx: 仿射变换的xx组件
   :type xx: float
   :param yx: 仿射变换的yx组件
   :type yx: float
   :param xy: 仿射变换的xy组件
   :type xy: float
   :param yy: 仿射变换的yy组件
   :type yy: float
   :param x0: 仿射变换的X组件
   :type x0: float
   :param y0: 仿射变换的Y组件
   :type y0: float

   使用 *xx, yx, xy, yy, x0, y0* 定义的仿射变换创建一个矩阵 *Matrix* 。仿射变换的公式如下::

     x_new = xx * x + xy * y + x0
     y_new = yx * x + yy * y + y0

   创建一个新的独立的矩阵::

     matrix = cairo.Matrix()

   要创建一个在X和Y轴变换(translates by)tx和ty的矩阵，可以向下面这样::

     matrix = cairo.Matrix(x0=tx, y0=ty)

   要创建一个在X和Y轴缩放(scale by)tx和ty的矩阵，可以向下面这样::

     matrix = cairo.Matrix(xx=sy, yy=sy)


   .. classmethod:: init_rotate(radians)

      :param radians: 旋转的角度，单位为弧度。旋转的方向从正X轴到正Y轴为正向的角度。
        再考虑到cairo中轴默认的方向，正角度为时钟旋转的方向。
      :type radians: float
      :returns: 设置旋转角度为 *radians* 的新的 *Matrix* 。


   .. method:: invert()

      :returns: 如果 *Matrix* 有逆矩阵（inverse），修改 *Matrix* 为其逆矩阵并返回None。
      :raises: 如果 *Matrix* 没有逆矩阵触发 :exc:`cairo.Error` 异常。

      将矩阵 *Matrix* 转换为其逆矩阵，并不是所有的转换矩阵都有逆矩阵，如果
      那么本函数会失败。
      （if the matrix collapses points
      together (it is *degenerate*), then it has no inverse and this function
      will fail.）


   .. method:: multiply(matrix2)

      :param matrix2: 另一个矩阵
      :type matrix2: cairo.Matrix
      :returns: 一个新的 *Matrix*

      两个仿射矩阵 *Matrix* 和 *matrix2* 相乘。新矩阵产生的效果为先将第一个矩阵变换 *Matrix* 作用于坐标再
      将第二个矩阵 *matrix2* 作用于坐标。

      结果与 *Matrix* 或 *matrix2* 不相同也是可以接受的。

      It is allowable for result to be identical to either *Matrix* or *matrix2*.


   .. method:: rotate(radians)

      :param radians: 旋转的角度，单位为弧度。旋转的方向从正X轴到正Y轴为正向的角度。
        再考虑到cairo中轴默认的方向，正角度为时钟旋转的方向。
      :type radians: float

      初始化 *Matrix* 为一个旋转 *radians* 弧度的一个转换。

   .. method:: scale(sx, sy)

      :param sx: X方向的缩放因子
      :type sx: float
      :param sy: Y方向的缩放因子
      :type sy: float

      对 *Matrix* 中的转换应用 *sx, sy* 缩放。新的转换的效果为首先以 *sx* 和 *sy* 缩放坐标，
      然后对坐标应用原来的转换。

   .. method:: transform_distance(dx, dy)

      :param dx: 空间向量的X组件
      :type dx: float
      :param dy: 空间向量的Y组件
      :type dy: float
      :returns: 转换后的空间向量 (dx,dy)
      :rtype: (float, float)

      使用矩阵 *Matrix* 转换空间向量 *(dx,dy)* 。其类似于
      :meth:`.transform_point` ，但是转换的转换组件被忽略。
      （except that the translation components of
      the transformation are ignored.）
      返回的向量是如此计算得出的::

        dx2 = dx1 * a + dy1 * c
        dy2 = dx1 * b + dy1 * d

      仿射变换是位置不变的，因此相同的向量总是转换为相同的向量。如果 *(x1,y1)*
      转换为 *(x2,y2)* 那么对于所有的 *x1* 和 *x2* *(x1+dx1,y1+dy1)* 会转换为 *(x1+dx2,y1+dy2)* 。

      Affine transformations are position invariant, so the same vector always
      transforms to the same vector. If *(x1,y1)* transforms to *(x2,y2)* then
      *(x1+dx1,y1+dy1)* will transform to *(x1+dx2,y1+dy2)* for all values
      of *x1* and *x2*.


   .. method:: transform_point(x, y)

      :param x: 点的X坐标
      :type x: float
      :param y: 点的Y坐标
      :type y: float
      :returns: 转换后的点 (x,y)
      :rtype: (float, float)

      使用 *Matrix* 转换点 *(x, y)* 。

   .. method:: translate(tx, ty)

      :param tx: X方向转换的数量
      :type tx: float
      :param ty: Y方向转换的数量
      :type ty: float

      对 *Matrix* 的转换应用 *tx, ty* 转换。新的转换的效果为先以  *tx* 和 *ty* 转换坐标，再
      应用原来的变换。
