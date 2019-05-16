#include <stdio.h>
#include <stdlib.h>
#include <dbus/dbus-glib.h>

static void callback_func(DBusGProxy *proxy, DBusGProxyCall *call_id, void *user_data)
{
    GError *err = NULL;
    gchar *str = NULL;
    GMainLoop *main_loop = user_data;

    /* 结束一条消息的收发，处理收到的消息 */
    dbus_g_proxy_end_call(proxy, call_id, &err, G_TYPE_STRING, &str, G_TYPE_INVALID);
    if (err != NULL) {
        g_print("Error in method call:%s\n", err->message);
        g_error_free(err);
    } else {
        g_print("Success, message:\n%s\n", str);
    }

    g_main_loop_quit(main_loop);
}

int main(int argc, char **argv)
{
    GError *error;
    DBusGConnection *conn;
    DBusGProxy *proxy;
    GMainLoop *main_loop;

    error = NULL;
    main_loop = g_main_loop_new(NULL, FALSE);
    /* connect session bus with dbus_g_get, or DBUS_BUS_SYSTEM connect system bus */
    conn = dbus_g_bus_get(DBUS_BUS_SESSION, &error);
    if (conn == NULL) {
        g_printerr("Failed to open connection to bus:%s\n", error->message);
        g_error_free(error);
        exit(1);
    }

    /* create a proxy object for  */
    proxy = dbus_g_proxy_new_for_name(conn,
            "org.freedesktop.Notifications", /* service */
            "/", /* path */
            "org.freedesktop.DBus.Introspectable"/* interface */
            );
    error = NULL;
    dbus_g_proxy_begin_call(proxy, "Introspect", callback_func, main_loop, NULL, G_TYPE_INVALID);
    g_main_loop_run(main_loop);

    return 0;
}
