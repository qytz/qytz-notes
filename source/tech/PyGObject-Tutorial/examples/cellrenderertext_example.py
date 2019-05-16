from gi.repository import Gtk

class CellRendererTextWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='CellRendererText Demo')

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(['Fedora', 'http://fedoraproject.org/'])
        self.liststore.append(['Slackware', 'http://www.slackware.com/'])
        self.liststore.append(['Sidux', 'http://sidux.com/'])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        col_txt = Gtk.TreeViewColumn('Text', renderer_text, text=0)
        treeview.append_column(col_txt)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property('editable', True)

        col_editabletxt = Gtk.TreeViewColumn('Editable Text',
                renderer_editabletext, text=1)
        treeview.append_column(col_editabletxt)
        renderer_editabletext.connect('edited', self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

win = CellRendererTextWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
