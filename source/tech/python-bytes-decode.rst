Python 3 Bytes.decode 遇到的问题
=========================================
使用 *Python 3* 的 `Subprocess` 模块执行 shell 命令，读取到的结果的类型是 `bytes` ，如果是文本需要转成 `str` 类型。

一般来说，Linux 的中文环境大都使用 *utf-8* 编码，我执行操作的系统也确实使用的 *utf-8* 编码，然后还是遇到了问题……

即使是使用了 *utf-8* 编码，我们的文件名仍然可能会产生乱码，比如我们执行 `ls` 可能会看到这样的文件名：:

    OITS??ѵ--????.mp4

而如果使用 `Subprocess` 模块执行 `ls` 命令，则 `result.decode("utf-8")` 会报 *UnicodeDecodeError* 异常，
初见这个问题我非常惊讶，应该 *utf-8* 可以编码所有的字符了吧，为啥我用 *utf-8* decode 还会出现这样的问题。

我觉得出现这个问题的原因很可能是，*Linux* 文件系统使用的 *utf-8* 编码保存文件名，但是 **该文件是从 Windows 的文件系统拷贝过来** ，
而 **Windows 文件系统的默认编码则是不是 utf-8** ，这样我们在 *shell* 执行 `ls` 命令时显示的就是乱码字符了，
因为我们的文件系统是存的 *utf-8* 编码的文件名，自然该文件名也是按照 *utf-8* 来解码输出。

要解决这个问题也不是很麻烦，参考资料 1 的答案很清楚，要么使用兼容的 *cp437/latin-1* 解码，要么使用 *utf-8* 解码时进行容错处理。

.. code:: python

   >>> result = b'\xc5\xe0\xd1\xb5--\xd1\xee\xc0\xa5.mp4'
   >>> result.decode("utf-8", errors="surrogateescape")
   '\udcc5\udce0ѵ--\udcd1\udcee\udcc0\udca5.mp4'
   >>> result.decode("cp437")
   '┼α╤╡--╤ε└Ñ.mp4'
   >>> result.decode("latin-1")
   'ÅàÑµ--ÑîÀ¥.mp4'


参考资料
--------------
#. `Convert bytes to a Python string <http://stackoverflow.com/a/27527728/6773188>`_
#. `PEP 383 -- Non-decodable Bytes in System Character Interfaces <https://www.python.org/dev/peps/pep-0383/>`_

