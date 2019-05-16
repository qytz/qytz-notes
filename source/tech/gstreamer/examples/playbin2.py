import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, Gtk, GObject

# important!!! needed by window.get_xid(), xvimagesink.set_window_handle.
from gi.repository import GdkX11, GstVideo

GObject.threads_init()
Gst.init(None)

class PlayBin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Audio Player')
        self.set_default_size(500, 400)
        self.connect('delete-event', Gtk.main_quit)

        vbox = Gtk.VBox()
        self.add(vbox)

        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.pack_start(self.entry, True, True, 0)
        self.button = Gtk.ToggleButton('Start')
        self.button.connect('clicked', self.start_stop)
        hbox.add(self.button)
        self.movie = Gtk.DrawingArea()
        vbox.add(self.movie)
        # build a palyer
        self.player = Gst.ElementFactory.make('playbin', 'player2')
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

        self.show_all()
        self.xid = self.movie.get_property('window').get_xid()

    def start_stop(self, widget):
        if self.button.get_active():
            filepath = self.entry.get_text()
            if os.path.isfile(filepath):
                self.button.set_label('Stop')
                self.player.set_property('uri', 'file://'+filepath)
                self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label('Start')

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label('Start')
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print('Error: %s' %err, debug)
            self.button.set_label('Start')

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            message.src.set_window_handle(self.xid)

win = PlayBin()
Gtk.main()
