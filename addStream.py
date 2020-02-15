# -*- coding: utf-8 -*-

from gi.repository import Gtk


class addStream(object):
    def add_stream_dialog(self, widget, StreamsList):
        """Dialog window to add a stream"""
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_modal(True)
        window.set_title('Settings')
        window.set_resizable(False)
        window.connect("destroy", lambda w: w.destroy())

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       homogeneous=False, spacing=5)
        window.add(vbox)

        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                        homogeneous=False, spacing=0)
        vbox.add(hbox1)

        NewKeyLabel = Gtk.Label('New stream label')
        NewKeyEntry = Gtk.Entry()
        NewKeyEntry.set_width_chars(20)
        hbox1.pack_start(NewKeyLabel, False, False, padding=5)
        hbox1.pack_end(NewKeyEntry, False, False, padding=5)

        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                        homogeneous=False, spacing=0)
        vbox.add(hbox2)

        NewCommandLabel = Gtk.Label('New stream command')
        NewCommandEntry = Gtk.Entry()
        NewCommandEntry.set_width_chars(30)
        hbox2.pack_start(NewCommandLabel, False, False, padding=5)
        hbox2.pack_end(NewCommandEntry, False, False, padding=5)

        hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                        homogeneous=False, spacing=0)
        vbox.add(hbox3)

        AddButton = Gtk.Button('Add')
        AddButton.connect('clicked', self.add_stream, window,
                          NewKeyEntry, NewCommandEntry, StreamsList)
        hbox3.pack_end(AddButton, False, False, padding=5)

        window.show_all()

    def add_stream(self, widget, window, key, command, StreamsList):
        """Add the stream key where needed"""
        newkey = key.get_text().strip()
        newcommand = command.get_text()
        if newkey == '' or newcommand == '' or \
                newkey in self.streams_dict.keys():
            key.modify_fg(Gtk.StateFlags.NORMAL, self.error_color)
        else:
            key.modify_fg(Gtk.StateFlags.NORMAL, None)
            newcommand = newcommand.strip()
            self.streams_dict[newkey] = newcommand

            StreamsList.insert_text(
                sorted(self.streams_dict.keys()).index(newkey), newkey)
            StreamsList.set_active(0)

            self.reset_streams_submenu()
            self.updateStreamsOnFile()
            window.destroy()
