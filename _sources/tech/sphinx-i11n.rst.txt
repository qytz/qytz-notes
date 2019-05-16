==============================
sphinx 生成本地化的文档
==============================

快速指南
===========
#. 使用 `pip install sphinx-intl` 或 `easy_install sphinx-intl` 安装 sphinx-intl。
#. 添加如下配置到你的 Sphinx 文档配置文件 conf.py::

        locale_dirs = ['locale/']   # path is example but recommended.gett
        ext_compact = False     # optional.

#. 根据原文档生成可供翻译的 pot 文件：:

        $ make gettext

   执行此命令会在 *_build/locale* 目录生成很多 pot 文件。

#. 生成 / 更新 locale_dir ::

        $ sphinx-intl update -p _build/locale -l zh_CN -l ja

   执行此命令会在 *locale_dir* 生成如下包含 po 文件的目录

   * ./locale/zh_CN/LC_MESSAGES/
   * ./locale/ja/LC_MESSAGES/

   支持的语言代码参考 http://www.sphinx-doc.org/en/stable/config.html#confval-language

   * bn – Bengali
   * ca – Catalan
   * cs – Czech
   * da – Danish
   * de – German
   * en – English
   * es – Spanish
   * et – Estonian
   * eu – Basque
   * fa – Iranian
   * fi – Finnish
   * fr – French
   * he – Hebrew
   * hr – Croatian
   * hu – Hungarian
   * id – Indonesian
   * it – Italian
   * ja – Japanese
   * ko – Korean
   * lt – Lithuanian
   * lv – Latvian
   * mk – Macedonian
   * nb_NO – Norwegian Bokmal
   * ne – Nepali
   * nl – Dutch
   * pl – Polish
   * pt_BR – Brazilian Portuguese
   * pt_PT – European Portuguese
   * ru – Russian
   * si – Sinhala
   * sk – Slovak
   * sl – Slovenian
   * sv – Swedish
   * tr – Turkish
   * uk_UA – Ukrainian
   * vi – Vietnamese
   * zh_CN – Simplified Chinese
   * zh_TW – Traditional Chinese

#. 翻译 *./locale/<lang>/LC_MESSAGES/* 目录下的 po 文件
#. 生成本地化的文档，你需要修改 conf.py 文档的 *language* 选项，或者在命令指定此选项：:

        $ make -e SPHINXOPTS="-D language='de'" html

如此，本地化的文档就在 *_build/html* 生成了。

参考资料
===========
#. `Sphinx Internationalization <http://www.sphinx-doc.org/en/stable/intl.html>`_

