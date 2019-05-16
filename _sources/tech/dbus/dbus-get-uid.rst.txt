==========================================
D-Bus系列之获取发送者UID及PID的方法
==========================================

获取PID及UID的原理
=========================
::

    org.freedesktop.DBus提供了一系列的消息，其中就有根据服务名获取进程PID及UID的接口
    "org.freedesktop.DBus", --服务
    "/org/freedesktop/DBus", --对象
    "org.freedesktop.DBus", --接口
    "GetConnectionUnixProcessID", --方法
     UINT32 GetConnectionUnixProcessID (in STRING bus_name);
    "GetConnectionUnixUser", --方法
    UINT32 GetConnectionUnixUser (in STRING bus_name);


QT DBUS获取的方法及示例
================================
QT DBUS提供了相关调用的封装:

#. const QDBusMessage & QDBusContext::message () const Returns the message that generated this call.
#. QString QDBusMessage::service () const Returns the name of the service or the bus address of the remote method call.
#. QDBusReply QDBusConnectionInterface::servicePid ( const QString & serviceName ) const Returns the Unix Process ID (PID) for the process currently holding the bus service serviceName.

例如：

.. code-block:: c++

    bool SomeMethod( const QString &name )
    {
         qDebug() << "PID is: " << connection().interface()->servicePid( message().service() );
    }


D-Bus glib绑定及GDBus
================================
D-Bus Glib 的绑定提供了获取发送者名字的方法：

.. code-block:: c

    const char *dbus_message_get_sender(DBusMessage *message);

但是没有提供获取进程PID及UID的方法，需自己编写代码调用GetConnectionUnixProcessID
和GetConnectionUnixUser方法。
好像GDbus也没有提供，只找到了g_dbus_message_get_sender()方法。

.. code-block:: c

    /* proxy for getting PID info */
    g_dbus_proxy_new_for_bus(G_BUS_TYPE_SYSTEM,
        G_DBUS_PROXY_FLAGS_DO_NOT_LOAD_PROPERTIES,
        NULL,
        "org.freedesktop.DBus",
        "/org/freedesktop/DBus",
        "org.freedesktop.DBus",
        NULL,
        (GAsyncReadyCallback)dbus_proxy_connect_cb,
        NULL);
    void
    dbus_proxy_connect_cb(GObject *source_object,
                   GAsyncResult *res,
                   gpointer user_data)
    {
        GError *error = NULL;

        dbus_proxy = g_dbus_proxy_new_finish (res, &error);
        if (error) {
            g_warning("dbus_proxy_connect_cb failed: %s", error->message);
            g_error_free(error);
            dbus_proxy = NULL;
        }
        else {
            g_debug("dbus_proxy_connect_cb succeeded");
        }
    }
    gboolean
    handle_request_sys_state (PowerdSource *obj, GDBusMethodInvocation     *invocation, int state)
    {
        // get the name of the dbus object that called us
        owner = g_dbus_method_invocation_get_sender(invocation);
        if (dbus_proxy) {
            result = g_dbus_proxy_call_sync(dbus_proxy,
                    "GetConnectionUnixProcessID",
                    g_variant_new("(s)", owner),
                    G_DBUS_CALL_FLAGS_NONE,
                    -1,
                    NULL,
                    &error);
            if (error) {
                g_error("Unable to get PID for %s: %s", owner, error->message);
                g_error_free(error);
                error = NULL;
            }
            else {
                g_variant_get(result, "(u)", &owner_pid);
                g_info("request is from pid %d\n", owner_pid);
            }
        }
        ...
    }

参考资料
===================
#. `D-Bus Specification <http://dbus.freedesktop.org/doc/dbus-specification.html>`_
#. `Getting the PID and Process Name From a dbus Caller in C  <http://www.mattfischer.com/blog/?p=494>`_
#. `Get sender PID from DBUS <http://stackoverflow.com/questions/9785610/get-sender-pid-from-dbus>`_
#. Qt doc及DBus-Glib、GDBus文档
