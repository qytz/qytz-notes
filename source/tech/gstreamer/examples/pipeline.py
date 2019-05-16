import sys, os

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

GObject.threads_init()
Gst.init(None)

class PipeMain(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='MP3-Player')
        self.resize(400, 200)
        self.connect('delete-event', Gtk.main_quit)
        vbox = Gtk.VBox()
        self.add(vbox)
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 1)
        self.button = Gtk.Button('Start')
        self.button.connect('clicked', self.start_stop)
        vbox.add(self.button)
        self.show_all()

        self.player = Gst.Pipeline()
        source = Gst.ElementFactory.make('filesrc', 'file-source')
        decoder = Gst.ElementFactory.make('mad', 'mp3-decoder')
        conv = Gst.ElementFactory.make('audioconvert', 'converter')
        sink = Gst.ElementFactory.make('alsasink', 'alsa-output')

        self.player.add(source)
        self.player.add(decoder)
        self.player.add(conv)
        self.player.add(sink)

        source.link(decoder)
        decoder.link(conv)
        conv.link(sink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    def start_stop(self, w):
        if self.button.get_label() == 'Start':
            filepath = self.entry.get_text()
            print(filepath)
            if os.path.isfile(filepath):
                self.button.set_label('Stop')
                self.player.get_by_name('file-source').set_property('location', filepath)
                self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label('Start')

    def on_message(self, bus, msg):
        t = msg.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label('Start')
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label('Start')
            err, debug = msg.parse_error()
            print('Error:%s' % err)

if __name__ == '__main__':
    PipeMain()
    Gtk.main()



