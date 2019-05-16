#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dbus/dbus-glib.h>
#include <dbus/dbus.h>
#include <unistd.h>

/*读取消息的参数，并且返回两个参数，一个是bool值stat，一个是整数level*/
void reply_to_method_call(DBusMessage * msg, DBusConnection * conn)
{
    DBusMessage * reply;
    DBusMessageIter arg;
    char * param = NULL;
    dbus_bool_t stat = TRUE;
    dbus_uint32_t level = 2010;
    dbus_uint32_t serial = 0;

    //从msg中读取参数，这个在上一次学习中学过
    if(!dbus_message_iter_init(msg,&arg)) {
        printf("Message has no args/n");
    } else if(dbus_message_iter_get_arg_type(&arg) != DBUS_TYPE_STRING) {
        printf("Arg is not string!/n");
    } else {
        dbus_message_iter_get_basic(&arg,& param);
    }
    if(param == NULL) return;

    //创建返回消息reply
    reply = dbus_message_new_method_return(msg);
    //在返回消息中填入两个参数，和信号加入参数的方式是一样的。这次我们将加入两个参数。
    dbus_message_iter_init_append(reply,&arg);
    if(!dbus_message_iter_append_basic(&arg,DBUS_TYPE_BOOLEAN,&stat)) {
        printf("Out of Memory!/n");
        exit(1);
    }
    if(!dbus_message_iter_append_basic(&arg,DBUS_TYPE_UINT32,&level)) {
        printf("Out of Memory!/n");
        exit(1);
    }
    //发送返回消息
    if( !dbus_connection_send(conn, reply, &serial)){
        printf("Out of Memory/n");
        exit(1);
    }
    dbus_connection_flush (conn);
    dbus_message_unref (reply);
}

/* 监听D-Bus消息，我们在上次的例子中进行修改 */
void listen_dbus()
{
    DBusMessage * msg;
    DBusMessageIter arg;
    DBusConnection * connection;
    DBusError err;
    int ret;
    char * sigvalue;

    dbus_error_init(&err);
    //创建于session D-Bus的连接
    connection = dbus_bus_get(DBUS_BUS_SESSION, &err);
    if(dbus_error_is_set(&err)){
        fprintf(stderr,"Connection Error %s/n",err.message);
        dbus_error_free(&err);
    }
    if(connection == NULL) {
        return;
    }
    //设置一个BUS name：test.wei.dest
    ret = dbus_bus_request_name(connection,"test.wei.dest",DBUS_NAME_FLAG_REPLACE_EXISTING,&err);
    if(dbus_error_is_set(&err)) {
        fprintf(stderr,"Name Error %s/n",err.message);
        dbus_error_free(&err);
    }
    if(ret != DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER) {
        return;
    }

    //要求监听某个singal：来自接口test.signal.Type的信号
    dbus_bus_add_match(connection,"type='signal',interface='test.signal.Type'",&err);
    dbus_connection_flush(connection);
    if(dbus_error_is_set(&err)){
        fprintf(stderr,"Match Error %s/n",err.message);
        dbus_error_free(&err);
    }

    while(TRUE){
        dbus_connection_read_write (connection,0);
        msg = dbus_connection_pop_message (connection);

        if(msg == NULL){
            sleep(1);
            continue;
        }

        if(dbus_message_is_signal(msg,"test.signal.Type","Test")){
            if(!dbus_message_iter_init(msg,&arg)) {
                fprintf(stderr,"Message Has no Param");
            } else if(dbus_message_iter_get_arg_type(&arg) != DBUS_TYPE_STRING) {
                g_printerr("Param is not string");
            } else {
                dbus_message_iter_get_basic(&arg,&sigvalue);
                printf("Got Singal with value : %s\n",sigvalue);
            }
        }else if(dbus_message_is_method_call(msg,"test.method.Type","Method")){
            //我们这里面先比较了接口名字和方法名字，实际上应当现比较路径
            if(strcmp(dbus_message_get_path (msg),"/test/method/Object") == 0) {
                reply_to_method_call(msg, connection);
            }
        }
        dbus_message_unref(msg);
    }
}

int main( int argc , char ** argv)
{
    listen_dbus();
    return 0;
}
