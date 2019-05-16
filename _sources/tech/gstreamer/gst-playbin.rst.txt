GStreamer系列之概览
=================================

playbin是一个高级别的，自动化的音视频播放器，一般来说，它会播放发送给他的任何
支持的多媒体数据。

playbin的内部看起来是这个样子的::

                                      playbin
          ____________________________________________________________________
         |                            ________________     _______________    |
         |                           |                |   |               |   |
         |                        ->-| optional stuff |->-| autoaudiosink |->-|->- Audio Output
         |    ________________   |   |________________|   |_______________|   |
         |   |                |--                                             |
  uri ->-|->-|  uridecodebin  |                                               |
         |   |________________|--     ________________     _______________    |
         |                       |   |                |   |               |   |
         |                        ->-| optional stuff |->-| autovideosink |->-|->- Video Output
         |                           |________________|   |_______________|   |
         |____________________________________________________________________|

"uri" 属性可以使用任何GStreamer插件支持的协议。playbin支持你将sink换成其他的，就
像我们在下面的例子中做的。一般来说，playbin总是会自动设置好你所要的一切，因此你
不要指定那些playbin没有实现的特性，开箱即用就不错的。

Example 1：播放起来
---------------------

.. literalinclude:: examples/playbin1.py
    :linenos:

由于playbin插件总是会自动播放音视频流，因此我们将视频重定向至 ``fakesink`` ，这
相当于Gstreamer中的 ``/dev/null`` 。你如果想要播放视频流，只需要注释掉这两行代码

.. literalinclude:: examples/playbin1.py
    :lines: 28-29

Example 2：控制视频的显示
------------------------------------
当然上面的例子在播放视频时总是会打开一个新的窗口，如果你想要在指定的窗口播放则
需要使用 ``enable_sync_message_emission()`` 方法。

.. literalinclude:: examples/playbin2.py
    :linenos:

Example 3：添加时间显示
--------------------------
我们可以让事情变的更有趣，我们将playbin的 *videosink* 切换为我们自己的GHostPad，
并在上面增加了一个时间显示的小元素。

.. literalinclude:: examples/playbin3.py
    :linenos:
