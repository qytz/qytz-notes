import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib
GObject.threads_init()
Gst.init(None)

class Play:
    def __init__(self):
        self.pipeline = Gst.Pipeline()

        self.audiotestsrc = Gst.ElementFactory.make('audiotestsrc', 'audio')
        # set property of element
        # self.audiotestsrc.set_property('freq', 300)
        print('freq:%d' %self.audiotestsrc.get_property('freq'))
        self.pipeline.add(self.audiotestsrc)

        self.sink = Gst.ElementFactory.make('alsasink', 'sink')
        self.pipeline.add(self.sink)

        self.audiotestsrc.link(self.sink)

        self.pipeline.set_state(Gst.State.PLAYING)

start = Play()
loop = GLib.MainLoop()
loop.run()
