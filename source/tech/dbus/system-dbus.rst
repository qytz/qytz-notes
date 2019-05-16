D-Bus系列之权限配置文件
===============================
D-Bus配置文件
D-Bus消息守护进程的配置文件配置了总线的类型，资源限制，安全参数等。
配置文件的格式并不是标准的一部分，也不保证向后兼容。。。

标准的系统总线和每会话总线在"/etc/dbus-1/system.conf" and "/etc/dbus-1/session.conf"，这两个文件
会包含system-local.conf或session-local.conf，因此你自己的配置应该放在单独的local文件中。

该配置文件的格式就是一个xml文档，且必须有如下类型声明：
 <!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN"
            "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">

<busconfig>
根元素

<type>
一般为system或session。

<include>
在当前位置包含该文件，如果是相对目录，则应为相对于当前配置文件所在目录，<include>有一个选项"ignore_missing=(yes|no)"，默认为no

<includedir>
在当前位置包含该目录所有的配置文件，目录中文件的包含顺序不定，且只有以".conf"结尾的文件才会被包含。

<user>
daemon运行的用户，可以为用户名或uid，如果守护进程无法切换到该用户就会自动退出，如果有多个<user>配置项，会采用最后一个。

<fork>
进程成为一个真正的守护进程。

<keep_umask>
若存在，守护进程在fork时会保留原来的umask。

<listen>
总线监听的地址，地址为包含传输地址加参数/选项的标准D-Bus格式，例如::

      <listen>unix:path=/tmp/foo</listen>
      <listen>tcp:host=localhost,port=1234</listen>

<auth>
指定授权机制。如果不存在，所有已知的机制都被允许。如果有多项配置，则所有列出的机制都被允许。

<servicedir>
添加扫描.service文件的目录，Service用于告诉总线如何自动启动一个程序，主要用于每用户的session bus。

<standard_session_servicedirs/> 等效于设定一系列的<servicedir/>元素， `"XDG Base Directory Specification" <http://freedesktop.org/wiki/Standards/basedir-spec>`_

<standard_system_servicedirs/>
设定标准的系统级service搜索目录，默认为/usr/share/dbus-1/system-services，
只用于/etc/dbus-1/system.conf.定义的系统级总线，放在其他配置文件中无效。

<servicehelper/>
设定setuid helper，使用设置的用户启动系统服务的守护进程，一般来说应该是dbus-daemon-launch-helper。
该选项仅用于系统总线。

<limit>
资源限制一般用于系统总线。
设置资源限制，例如::

         <limit name="max_message_size">64</limit>
         <limit name="max_completed_connections">512</limit>

可用的限制名有::
             
             "max_incoming_bytes"         : total size in bytes of messages
                                            incoming from a single connection
             "max_incoming_unix_fds"      : total number of unix fds of messages
                                            incoming from a single connection
             "max_outgoing_bytes"         : total size in bytes of messages
                                            queued up for a single connection
             "max_outgoing_unix_fds"      : total number of unix fds of messages
                                            queued up for a single connection
             "max_message_size"           : max size of a single message in
                                            bytes
             "max_message_unix_fds"       : max unix fds of a single message
             "service_start_timeout"      : milliseconds (thousandths) until
                                            a started service has to connect
             "auth_timeout"               : milliseconds (thousandths) a
                                            connection is given to
                                            authenticate
             "max_completed_connections"  : max number of authenticated connections
             "max_incomplete_connections" : max number of unauthenticated
                                            connections
             "max_connections_per_user"   : max number of completed connections from
                                            the same user
             "max_pending_service_starts" : max number of service launches in
                                            progress at the same time
             "max_names_per_connection"   : max number of names a single
                                            connection can own
             "max_match_rules_per_connection": max number of match rules for a single
                                               connection
             "max_replies_per_connection" : max number of pending method
                                            replies per connection
                                            (number of calls-in-progress)
             "reply_timeout"              : milliseconds (thousandths)
                                            until a method call times out

<policy>
定义用于一组特定连接的安全策略，策略由<allow>和<deny>元素组成。
策略一般用于系统总线，模拟防火墙的功能来只允许期望的连接。
当前系统总线的默认策略会阻止发送方法调用和获取总线名字，其他的如消息回复、信号等是默认允许的。

通常来说，最好是保证系统服务尽可能的小，目标程序在自己的进程中运行并且提供一个总线名字来提供服务。
<allow>规则使得程序可以设置总线名字，<send_destination>允许一些或所有的uid访问我们的服务。

<policy>元素可以有下面四个属性中的一个：
context="(default|mandatory)"
at_console="(true|false)"
user="username or userid"
group="group name or gid"

策略以下面的规则应用到连接：
- 所有 context="default" 的策略被应用
- 所有 group="connection's user's group" 的策略以不定的顺序被应用
- 所有 user="connection's auth user" 的策略以不定顺序被应用
- 所有 at_console="true" 的策略被应用
- 所有 at_console="false" 的策略被应用
- 所有 context="mandatory" 的策略被应用
后应用的策略会覆盖前面的策略。

<allow>和<deny>出现在<policy>元素下面，<deny>禁止一些动作，而<allow>则创建上面<deny>元素的一些例外。
这两个元素可用的属性包括：

         send_interface="interface_name"
          send_member="method_or_signal_name"
          send_error="error_name"
          send_destination="name"
          send_type="method_call" | "method_return" | "signal" | "error"
          send_path="/path/name"

          receive_interface="interface_name"
          receive_member="method_or_signal_name"
          receive_error="error_name"
          receive_sender="name"
          receive_type="method_call" | "method_return" | "signal" | "error"
          receive_path="/path/name"

          send_requested_reply="true" | "false"
          receive_requested_reply="true" | "false"

          eavesdrop="true" | "false"

          own="name"
          own_prefix="name"
          user="username"
          group="groupname"


send_destination跟receive_sender是指发送到目的为或者收到来自于该名字的owner，而不是该名字。因此
如果一个连接有三个服务A、B、C，如果拒绝发送到A，那么发送到B和C也不行。
其他的send_*和receive_*则匹配消息头的字段。
