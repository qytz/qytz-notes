#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dbus/dbus-glib.h>
#include <dbus/dbus.h>
#include <unistd.h>

void listen_signal()
{
    DBusMessage * msg;
    DBusMessageIter arg;
    DBusConnection * connection;
    DBusError err;
    int ret;
    char * sigvalue;

    //步骤1:建立与D-Bus后台的连接
    dbus_error_init(&err);
    connection = dbus_bus_get(DBUS_BUS_SESSION, &err);
    if(dbus_error_is_set(&err)) {
        fprintf(stderr,"Connection Error %s\n",err.message);
        dbus_error_free(&err);
    }
    if(connection == NULL) {
        return;
    }

    //步骤2:给连接名分配一个可记忆名字test.singal.dest作为Bus name，这个步骤不是必须的,但推荐这样处理
    ret = dbus_bus_request_name(connection,"test.singal.dest",DBUS_NAME_FLAG_REPLACE_EXISTING,&err);
    if(dbus_error_is_set(&err)) {
        fprintf(stderr,"Name Error %s\n",err.message);
        dbus_error_free(&err);
    }
    if(ret != DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER) {
        return;
    }

    //步骤3:通知D-Bus daemon，希望监听来行接口test.signal.Type的信号
    dbus_bus_add_match(connection,"type='signal',interface='test.signal.Type'",&err);
    //实际需要发送东西给daemon来通知希望监听的内容，所以需要flush
    dbus_connection_flush(connection);
    if(dbus_error_is_set(&err)) {
        fprintf(stderr,"Match Error %s\n",err.message);
        dbus_error_free(&err);
    }

    //步骤4:在循环中监听，每隔开1秒，就去试图自己的连接中获取这个信号。这里给出的是从连接中获取任何消息的方式，所以获取后去检查一下这个消息是否我们期望的信号，并获取内容。我们也可以通过这个方式来获取method call消息。
    while(1) {
        dbus_connection_read_write(connection,0);
        msg = dbus_connection_pop_message (connection);
        if(msg == NULL){
            sleep(1);
            continue;
        }

        if(dbus_message_is_signal(msg,"test.signal.Type","Test") ){
            if(!dbus_message_iter_init(msg,&arg)) {
                fprintf(stderr,"Message Has no Param");
            } else if(dbus_message_iter_get_arg_type(&arg) != DBUS_TYPE_STRING) {
                g_printerr("Param is not string");
            } else {
                dbus_message_iter_get_basic(&arg,&sigvalue);
                printf("Got Singal with value : %s\n",sigvalue);
            }
        }
        dbus_message_unref(msg);
    }//End of while

    return ;
}

int main( int argc , char ** argv){
    listen_signal();
    return 0;
}
