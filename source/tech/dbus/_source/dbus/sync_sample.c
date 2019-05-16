#include <stdio.h>
#include <stdlib.h>
#include <dbus/dbus-glib.h>

int main(int argc, char **argv)
{
    GError *error;
    DBusGConnection *conn;
    DBusGProxy *proxy;
    char *str;

    /* gtype init */
    error = NULL;
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
    if (!dbus_g_proxy_call(proxy, "Introspect", &error, G_TYPE_INVALID, G_TYPE_STRING, &str, G_TYPE_INVALID)) {
        if (error->domain == DBUS_GERROR && error->code == DBUS_GERROR_REMOTE_EXCEPTION) {
            g_printerr("Caught remote method exception:%s-%s\n", dbus_g_error_get_name(error), error->message);
        } else {
            g_printerr("Error:%s\n", error->message);
        }
        g_error_free(error);
        exit(1);
    }

    g_print("Message Method return from bus:\n%s\n", str);
    g_free(str);
    g_object_unref(proxy);
    exit(1);

    return 0;
}
