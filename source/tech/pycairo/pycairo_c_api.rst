.. highlightlang:: c


*******************
Pycairo 的 C API
*******************

.. currentmodule:: cairo

这篇手册描述了给那些想使用pycairo来写扩展模块的C和C++程序员使用的API。


.. _api-includes:

访问Pycairo 的 C API
===========================
下面的例子展示了如何导入 pycairo的API::

  #include "py3cairo.h"

  PyMODINIT_FUNC
  PyInit_client(void)
  {
    PyObject *m;

    m = PyModule_Create(&clientmodule);
    if (m == NULL)
        return NULL;
    if (import_cairo() < 0)
        return NULL;
    /* additional initialization can happen here */
    return m;
  }



Pycairo 对象
===============
Objects::

  PycairoContext
  PycairoFontFace
  PycairoToyFontFace
  PycairoFontOptions
  PycairoMatrix
  PycairoPath
  PycairoPattern
  PycairoSolidPattern
  PycairoSurfacePattern
  PycairoGradient
  PycairoLinearGradient
  PycairoRadialGradient
  PycairoScaledFont
  PycairoSurface
  PycairoImageSurface
  PycairoPDFSurface
  PycairoPSSurface
  PycairoSVGSurface
  PycairoWin32Surface
  PycairoXCBSurface
  PycairoXlibSurface


Pycairo Types
=============
Types::

  PyTypeObject *Context_Type;
  PyTypeObject *FontFace_Type;
  PyTypeObject *ToyFontFace_Type;
  PyTypeObject *FontOptions_Type;
  PyTypeObject *Matrix_Type;
  PyTypeObject *Path_Type;
  PyTypeObject *Pattern_Type;
  PyTypeObject *SolidPattern_Type;
  PyTypeObject *SurfacePattern_Type;
  PyTypeObject *Gradient_Type;
  PyTypeObject *LinearGradient_Type;
  PyTypeObject *RadialGradient_Type;
  PyTypeObject *ScaledFont_Type;
  PyTypeObject *Surface_Type;
  PyTypeObject *ImageSurface_Type;
  PyTypeObject *PDFSurface_Type;
  PyTypeObject *PSSurface_Type;
  PyTypeObject *SVGSurface_Type;
  PyTypeObject *Win32Surface_Type;
  PyTypeObject *XCBSurface_Type;
  PyTypeObject *XlibSurface_Type;


Functions
=========

.. c:function::  cairo_t * PycairoContext_GET(obj)

   从PycairoContext获取C语言的cairo_t 对象


.. c:function::  PyObject * PycairoContext_FromContext(cairo_t *ctx, PyTypeObject *type, PyObject *base)


.. c:function::  PyObject * PycairoFontFace_FromFontFace(cairo_font_face_t *font_face)


.. c:function::  PyObject * PycairoFontOptions_FromFontOptions(cairo_font_options_t *font_options)


.. c:function::  PyObject * PycairoMatrix_FromMatrix(const cairo_matrix_t *matrix)


.. c:function::  PyObject * PycairoPath_FromPath(cairo_path_t *path)


.. c:function::  PyObject * PycairoPattern_FromPattern(cairo_pattern_t *pattern, PyObject *base)


.. c:function::  PyObject * PycairoScaledFont_FromScaledFont(cairo_scaled_font_t *scaled_font)


.. c:function::  PyObject * PycairoSurface_FromSurface(cairo_surface_t *surface, PyObject *base)


.. c:function::  int PycairoCheck_Status(cairo_status_t status)
