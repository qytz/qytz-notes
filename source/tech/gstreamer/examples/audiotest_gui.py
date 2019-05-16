import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
GObject.threads_init()
Gst.init(None)

class Play:
    def __init__(self):
        handlers = {
                'on_play_clicked' : self.on_play,
                'on_stop_clicked' : self.on_stop,
                'on_quit_clicked' : self.on_quit,
                'on_freq_changed' : self.on_freq_change,
        }

        self.builder = Gtk.Builder()
        self.builder.add_from_file('audiotest_gui.glade')
        self.builder.connect_signals(handlers)


        # Gstreamer gays
        self.pipeline = Gst.Pipeline()

        self.audiotestsrc = Gst.ElementFactory.make('audiotestsrc', 'audio')
        freq = self.audiotestsrc.get_property('freq')
        self.pipeline.add(self.audiotestsrc)

        self.sink = Gst.ElementFactory.make('alsasink', 'sink')
        self.pipeline.add(self.sink)

        self.audiotestsrc.link(self.sink)

        entry = self.builder.get_object('entry1')
        entry.set_text(str(freq))
        win = self.builder.get_object('window1')
        win.connect('delete-event', Gtk.main_quit)
        win.show_all()

    def on_freq_change(self, widget, *args):
        print('freq changde...')
        entry = self.builder.get_object('entry1')
        freq = entry.get_text()
        self.audiotestsrc.set_property('freq', int(freq))

    def on_play(self, *args):
        print('palying...')
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_stop(self, *args):
        print('stoped.')
        self.pipeline.set_state(Gst.State.NULL)
        #self.pipeline.set_state(Gst.State.PAUSED)
        #self.pipeline.set_state(Gst.State.READY)

    def on_quit(self, *args):
        Gtk.main_quit()

start = Play()
Gtk.main()
