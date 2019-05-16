#!/usr/bin/eny python
#coding:utf-8

from  gi.repository import Gtk

class ButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Button Demo')
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button('Click Me')
        button.connect('clicked', self.on_click_me_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button(stock=Gtk.STOCK_OPEN)
        button.connect('clicked', self.on_open_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button('_Close', use_underline=True)
        button.connect('clicked', self.on_close_clicked)
        hbox.pack_start(button, True, True, 0)

    def on_click_me_clicked(self, button):
        print '"click me" button was clicked'

    def on_open_clicked(self, button):
        print '"open" button was clicked'

    def on_close_clicked(self, button):
        print 'Closing application'
        Gtk.main_quit()

wind = ButtonWindow()
wind.connect('delete-event', Gtk.main_quit)
wind.show_all()
Gtk.main()
