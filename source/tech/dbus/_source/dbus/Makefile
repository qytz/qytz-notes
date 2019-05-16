CC=gcc

CFLAGS += `pkg-config --cflags dbus-glib-1 glib-2.0`
LIBS += `pkg-config --libs dbus-glib-1 glib-2.0`

all: sync_sample async_sample signal_send signal_recv method_service method_call

async_sample: async_sample.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

sync_sample: sync_sample.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

signal_send: signal_send.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

signal_recv: signal_recv.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

method_service: method_service.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

method_call:method_call.c
	$(CC) -Wall -g $(CFLAGS) $< $(LIBS) -o $@

clean:
	rm -f sync_sample async_sample signal_send signal_recv method_service method_call
