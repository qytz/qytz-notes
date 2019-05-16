处理字符串相关问题
========================

本章介绍在Python 2.x、Python 3.x及Gtk+中字符串是如何表示的，讨论当使用字符串时通常可能会遇到的问题。

字符串之深度定义
----------------
从概念上来讲，字符串是一串如 ’A‘、‘B’、‘C’或者‘É’ 这样的字符的列表。 **字符** 呢，其实只是抽象的代表，
其意义依赖于他们所用于的语言和上下文环境。Unicode标准定义了字符是如何有码位
（code points，觉得译为代码点太别扭了，嗯，码位貌似还行。。。）来表示的。例如上面哪些字符即是由
U+0041, U+0042, U+0043, and U+00C9这些码位来表示的。码位是一个从0到0x10FFFF之间的数。

之前有提到（有吗？），把字符串作为系列字符的列表来理解很抽象。为了将这抽象而无语的表示转换成一系列的字节表示，
Unicode字符串必须要被 **编码** 。最简单的ASCII编码方法是这样的：

1. 如果码位小于128，每个字节的值即与码位的值相同。
2. 如果码位大于等于128，这个Unicode字符串就不能按照ASCII来编码了。（Python在这种情况下会产生 :exc:`UnicodeEncodeError` 异常。）

尽管ASCII编码很简单，但其只能编码128个不同的字符，对我们亚洲那里够呢。
那么其中最常用的解决了这个问题的编码方法就是UTF-8了（可以处理所有Unicode码位）。
UTF代表"Unicode Transformation Format"，而 '8' 则指这种编码方式使用八位来编码。


Python 2
--------

Python 2.x 中的Unicode支持
+++++++++++++++++++++++++++++++
Python 2 中有两种不同类型的对象可以用来表示字符串： :class:`str` 和 :class:`unicode` 。
后者的实例用来表示Unicode字符串，而 :class:`str` 则是字节表示（即编码后的字符串）。 
Python 中表示Unicode字符串为16位或者32位的整数，
这依赖于Python解释器是怎样被编译的。Unicode字符串可以使用 :meth:`unicode.encode` 被编码为八位的字符串::

	>>> unicode_string = u"Fu\u00dfb\u00e4lle"
	>>> print unicode_string
	Fußbälle
	>>> type(unicode_string)
	<type 'unicode'>
	>>> unicode_string.encode("utf-8")
	'Fu\xc3\x9fb\xc3\xa4lle'

Python中的八位字符串有一个 :meth:`str.decode` 方法可以以给定的方法来翻译字符串::

	>>> utf8_string = unicode_string.encode("utf-8")
	>>> type(utf8_string)
	<type 'str'>
	>>> u2 = utf8_string.decode("utf-8")
	>>> unicode_string == u2
	True

不幸的是，如果八位的字符串只包含七位的（ASCII字符）字节Python 2.x 允许你混淆
:class:`unicode` 和 :class:`str` ，但如果字符串包含非ASCII字符时则会产生
:exc:`UnicodeDecodeError` ::

	>>> utf8_string = " sind rund"
	>>> unicode_string + utf8_string
	u'Fu\xdfb\xe4lle sind rund'
	>>> utf8_string = " k\xc3\xb6nnten rund sein"
	>>> print utf8_string
	 könnten rund sein
	>>> unicode_string + utf8_string
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 2: ordinal not in range(128)

GTK+中的Unicode
++++++++++++++++++
GTK+中所有的文本都使用UTF-8编码。这意味着如果你调用一个返回字符串的方法你总是会得到一个 :class:`str` 类型的实例。
对于需要一个或多个字符串参数的方法也是一样的，它们（指参数们）必须是UTF-8编码的。
但是为了方便，作为参数时PyGObject总是自动的将 :class:`unicode` 实例转换 :class:`str`::

	>>> from gi.repository import Gtk
	>>> label = Gtk.Label()
	>>> unicode_string = u"Fu\u00dfb\u00e4lle"
	>>> label.set_text(unicode_string)
	>>> txt = label.get_text()
	>>> type(txt), txt
	(<type 'str'>, 'Fu\xc3\x9fb\xc3\xa4lle')
	>>> txt == unicode_string
	__main__:1: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
	False

注意最后的警告。尽管我们以一个unicode实例作为参数来调用 :meth:`Gtk.Label.set_text` ，
:meth:`Gtk.Label.get_text` 总是返回一个 :class:`str` 实例。因此， ``txt`` 和 ``unicode_string`` 并 **不** 相等。

如果你要使用gettext来国际化你的程序，这尤其重要。对所有语言你需要确保
`gettext <http://docs.python.org/library/gettext.html>`_ 会返回UTF-8编码的字符串。
通常建议不要在GTK+程序中使用 :class:`unicode` 对象，而是只使用UTF-8编码的 :class:`str` 对象，
因为GTK+并没有完全的整合 :class:`unicode` 对象。
否则，你每次调用GTK+方法都要解码返回值为Unicode字符串::

	>>> txt = label.get_text().decode("utf-8")
	>>> txt == unicode_string
	True

Python 3
--------

Python 3.x的Unicode支持
++++++++++++++++++++++++++++
自从Python 3.0开始，所有的字符串都以 :class:`str` 类型的实例来存储为Unicode了。
编码后的字符串则是以二进制形式为 :class:`bytes` 类型的实例。从概念上来讲， :class:`str` 代表 *文本* ，
而 :class:`bytes` 则代表 *数据* 。使用 :meth:`str.encode` 将 :class:`str` 转换为 :class:`bytes` 。
使用:meth:`bytes.decode` 将 :class:`bytes` 转换为 :class:`str` 。
当然，也就不能再混淆Unicode字符串和编码后的字符串了，因为这样会产生 :exc:`TypeError`::

	>>> text = "Fu\u00dfb\u00e4lle"
	>>> data = b" sind rund"
	>>> text + data
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	TypeError: Can't convert 'bytes' object to str implicitly
	>>> text + data.decode("utf-8")
	'Fußbälle sind rund'
	>>> text.encode("utf-8") + data
	b'Fu\xc3\x9fb\xc3\xa4lle sind rund'

GTK+中的Unicode
+++++++++++++++++++
结果，在Python 3.x中事情就变的非常简单了，因为如果你传递一个字符串给一个方法或一个方法返回了字符串，
PyGObject会自动的编码为/解码为UTF-8。字符串或者 *文本* 会自动翻译为 :class:`str` 的实例 ::

	>>> from gi.repository import Gtk
	>>> label = Gtk.Label()
	>>> text = "Fu\u00dfb\u00e4lle"
	>>> label.set_text(text)
	>>> txt = label.get_text()
	>>> type(txt), txt
	(<class 'str'>, 'Fußbälle')
	>>> txt == text
	True

References
----------
`What's new in Python 3.0 <http://docs.python.org/py3k/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit>`_
描述了能清晰的区分文本和数据的新概念。

`Unicode HOWTO <http://docs.python.org/howto/unicode.html>`_ 
讨论了Python 2.x对Unicode的支持，并解释了人们使用Unicode时可能会遇到的问题。

`Unicode HOWTO for Python 3.x <http://docs.python.org/dev/howto/unicode.html>`_
讨论了Python 3.x对Unicode的支持。

`UTF-8 encoding table and Unicode characters <http://www.utf8-chartable.de>`_ 包含了一个Unicode的码位和其UTF-8编码的对应关系。
