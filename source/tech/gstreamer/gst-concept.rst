GStreamer系列之几个入门概念
=======================================

Overview
---------
GStreamer是一个多媒体框架，它可以允许你轻易地创建、编辑与播放多媒体文件，这是
通过创建带有很多特殊的多媒体元素的管道来完成的。

管道-pipeline
---------------
GStreamer的工作方式非常简单，你只需创建一个包含很多元素的管道，这与Linux命令行
的管道非常类似，例如，一般命令行的管道是这样的::

    foo@bar:~$ ps ax | grep "apache" |wc -l

这个命令首先捕获一个进程列表然后返回名字包含 "apache" 的进程并传递给 wc 命令并
统计出行数。我们可以看出每一个使用 ``|`` 连接，并且 ``|`` 左边的命令的输出传递
给其右边的命令作为输入。

GStreamer的工作方式与此类似，GStreamer中你将很多元素串联起来，每一个元素都完成
某些特定的事。我们来演示一下::

    gst-launch-1.0 filesrc location=越单纯越幸福.mp3 ! decodebin ! audioconvert ! alsasink

运行这条命令你就可以听到动听的音乐了，当然前提是你的当前目录有这个音乐文件。

``gst-launch-1.0`` 可以用来运行 GStreamer 管道，你只需要将需要使用的元素一个一个
传递给它就可以了，每一个命令使用 ``!`` 来连接。此处你可以把 ``!`` 当作命令行里
的 ``|`` 。上面那条命令包含了几个元素，我们简单解释一下：
a. filesrc——这个元素从本地磁盘加载了一个文件，使用该元素时你设置了 *location*
属性指向了音乐文件，关于属性我们后边聊。
b. decodebin——我们需要从 *filesrc* 解码，因此我们使用了这个元素。这个元素是一个
聪明的小家伙，它会自动检测文件的类型并在后台构造一些GStreamer元素来解码。因此，
此处对于 mp3 你可以使用 mad 代替之试一下。
c. audioconvert——一个声音文件中有各种各样的信息，每种信息传递到喇叭都是不同的，
因此要使用此元素来做一下转换。
d. alsasink——这个元素做的事很简单，就是把你的音频使用ALSA传递给你的声卡。

文章写到这里，我们就可以使用管道来做各种试验了，但首先我们要知道有那些元素可以
使用啊::

    foo@bar:~$ gst-inspect-1.0

这个命令列出了可用的元素，你也可以使用该命令查看某一元素的详细信息，例如 filesrc
元素::

    foo@bar:~$ gst-inspect-1.0 filesrc

下面介绍一些GStreamer的相关术语，一些人可能很快就会对 *pad*, *cap* 这些术语搞晕，
就不要说 *bin* 和 *ghost pad* 了。其实这些术语都相当的简单。。。

元素element
-------------
其实我们已经讨论了管道，而元素就在管道上。每一个元素都有很多属性用来设置该元素。
例如， *volume* 元素（设置管道的音量）有一个熟悉 **volume** 可以设置音量或者静音。
当你创建自己的管道时就要给很多的元素设置属性。

pad
----
每一个元素都有虚拟的插头供数据流入和流出，即pad。如果你把元素看作一个对输入的
数据做一些处理的黑盒。在盒子的左右两边就是插孔了，你可以插入电缆向盒子传入信息，
这就是pad要做的事。绝大多数元素有一个输入pad（叫做sink）和一个输出pad(叫做src)。
因此，我们上面的管道看起来是这样的::

    [src] ! [sink src] ! [sink src] ! [sink]

最左边的元素只有一个src pad用来提供信息（如filesrc）。接下来的几个元素接收信息并
做一些处理，因此他们有sink和src pad（例如decodebin和audiocovert），最后一个元素
只接收信息（例如alsasink）。当你使用 ``gst-inspect-1.0`` 命令查看一个元素的详细
信息时，就会列出该元素的pad信息。

注意可能与平时大家认为的概念有些不同的是，src pad是用来发送数据的端点，即数据的
输出端；而sink pad是用来接收数据的端点，即数据的输入端。

而且，一般来说，src pad只能连接到sink pad。当然，没有例外的规则是不存在的，
ghost pad两端就要连接相同类型的pad，具体请参考后面的例子吧。

cap
-----
我们已经了解了pad和从管道第一个元素到最后一个元素的数据流是怎么回事了，那么我们
来讨论下 *cap* 。每一个元素都有特定的cap，cap是指该元素可以接收什么样的信息（
例如是接收音频还是视频）。你可以把cap看成是电源插座上其可以接受什么范围电压的规则。

bin
-----
很多人不理解bin，其实它很简单。bin就是一种便捷的方式，可以把很多个元素放进一个
容器中。例如你有很多个元素用来解码视频并对其使用一些效果。要使事情变得简单一些，
你可以把这些元素放进一个bin（就像一个容器）中，以后你就可以使用bin来引用这些元素了。
这样其实bin变成了一个元素，例如你的管道是 ``a ! b ! c ! d`` ，你可以把他们放进
mybin，这样当你使用mybin时其实是引用了 ``a ! b ! c ! d`` 。

ghost pad
------------
当你创建了一个bin并在里面放置了很多元素时，该bin变成了你自定义的元素，该元素按
顺序调用里面的元素。要做到这样，你的bin很自然地需要它自己的pad，它自己的pad会挂接
到bin里面元素的pad上，这就是 *ghost pad* 了。当你创建一个bin时，你创建了ghost pad
并告诉他们要去挂接里面哪一个元素。

Example
-------------
话不多说，上例子。

.. literalinclude:: examples/audiotest.py
    :linenos:

上面这个例子很简单，使用命令行的例子来写::

    gst-launch-1.0 audiotestsrc ! alsasink
    gst-launch-1.0 audiotestsrc freq=300 ! alsasink

我们把上面的例子加上GUI，让它看起来是一个真正的桌面应用。

使用Glade构建的应用界面：

.. literalinclude:: examples/audiotest_gui.glade
    :linenos:

程序的处理代码：

.. literalinclude:: examples/audiotest_gui.py
    :linenos:

参考文献
---------
`Getting started with GStreamer with Python <http://www.jonobacon.org/2006/08/28/getting-started-with-gstreamer-with-python/>`_

