from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

icons = ['gtk-cut', 'gtk-paste', 'gtk-copy']

class IconViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='IconView Demo')
        self.set_default_size(200, 200)

        liststore = Gtk.ListStore(Pixbuf, str, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.set_tooltip_column(2)

        for icon in icons:
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
            liststore.append([pixbuf, 'Label', icon])

        self.add(iconview)

win = IconViewWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
