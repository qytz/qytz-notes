#!/usr/bin/env python
#coding:utf-8

from gi.repository import Gtk

class LinkButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='LinkButton Demo')
        self.set_border_width(10)

        button = Gtk.LinkButton('http://www.gtk.org', 'Visit Gtk+ homepage')
        self.add(button)

wind = LinkButtonWindow()
wind.connect('delete-event', Gtk.main_quit)
wind.show_all()
Gtk.main()
