import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, Gtk, GObject
GObject.threads_init()
Gst.init(None)

class PlayBin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Audio Player')
        self.set_default_size(300, -1)
        self.connect('delete-event', Gtk.main_quit)

        vbox = Gtk.VBox()
        self.add(vbox)

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)
        self.button = Gtk.ToggleButton('Start')
        self.button.connect('clicked', self.start_stop)
        vbox.add(self.button)
        self.show_all()

        # build a palyer
        self.player = Gst.ElementFactory.make('playbin', 'player')
        # we don't need video output
        #fakesink = Gst.ElementFactory.make('fakesink', 'fakesink')
        #self.player.set_property('video-sink', fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

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

win = PlayBin()
Gtk.main()
