from gi.repository import Gtk, Gdk

class ClipboardWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Clipboard Demo')

        grid = Gtk.Grid()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.entry = Gtk.Entry()
        self.image = Gtk.Image.new_from_stock(Gtk.STOCK_STOP, Gtk.IconSize.MENU)

        button_copy_text = Gtk.Button('Copy Text')
        button_paste_text = Gtk.Button('Paste Text')
        button_copy_image = Gtk.Button('Copy Image')
        button_paste_image = Gtk.Button('Paste Image')

        grid.attach(self.entry, 0, 0, 1, 1)
        grid.attach_next_to(self.image, self.entry, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(button_copy_text, self.entry, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(button_paste_text, button_copy_text, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(button_copy_image, button_copy_text, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(button_paste_image, button_paste_text, Gtk.PositionType.BOTTOM, 1, 1)

        button_copy_text.connect('clicked', self.copy_text)
        button_paste_text.connect('clicked', self.paste_text)
        button_copy_image.connect('clicked', self.copy_image)
        button_paste_image.connect('clicked', self.paste_image)

        self.add(grid)

    def copy_text(self, widget):
        self.clipboard.set_text(self.entry.get_text(), -1)

    def paste_text(self, widget):
        text = self.clipboard.wait_for_text()
        if text != None:
            self.entry.set_text(text)
        else:
            print 'No Text on the clipboard'

    def copy_image(self, widget):
        if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
            self.clipboard.set_image(self.image.get_pixbuf())
        else:
            print 'No image has been pasted yet'

    def paste_image(self, widget):
        image = self.clipboard.wait_for_image()
        if image != None:
            self.image.set_from_pixbuf(image)
        else:
            print 'No Image on the clipboard'

win = ClipboardWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
