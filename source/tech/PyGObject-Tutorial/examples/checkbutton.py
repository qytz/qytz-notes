#!/usr/bin/eny python
#coding:utf-8

from gi.repository import Gtk

class ToggleButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ToggleButton Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.CheckButton("Button 1")
        button.connect('toggled', self.on_button_toggled, '1')
        hbox.pack_start(button, True, True, 0)

        button = Gtk.CheckButton("B_utton 2", use_underline=True)
        button.set_active(True)
        button.connect('toggled', self.on_button_toggled, '2')
        hbox.pack_start(button, True, True, 0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = 'on'
        else:
            state = 'off'
        print 'Button', name, 'was tunned', state

wind = ToggleButtonWindow()
wind.connect('delete-event', Gtk.main_quit)
wind.show_all()
Gtk.main()
