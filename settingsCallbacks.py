# -*- coding: utf-8 -*-

from gi.repository import Gtk


class settingsCallbacks(object):
    def notifications(self, widget, some):
        """Turn notifications On/Off"""
        self.NotificationOn = not self.NotificationOn
        self.updateSettings()

    def update_recent_num(self, widget, RecentStreamsNumEntry):
        """Update the number of recent streams"""
        try:
            self.recent_streams_num = int(RecentStreamsNumEntry.get_text())
            if self.recent_streams_num >= 0:
                RecentStreamsNumEntry.modify_fg(Gtk.StateFlags.NORMAL, None)
                while len(self.recent_streams) > self.recent_streams_num:
                    self.recent_streams.pop(-1)
                self.update_recent_menu()
                self.updateRecentOnFile()
                self.updateSettings()
            else:
                RecentStreamsNumEntry.modify_fg(
                    Gtk.StateFlags.NORMAL,
                    self.error_color)
        except:
            print("Input is not good")

    def update_current(self, widget, StreamsList, StreamCommand):
        """Save the command for the current stream"""
        self.streams_dict[StreamsList.get_active_text()] = \
            StreamCommand.get_text()
        self.updateStreamsOnFile()

    def restore_current(self, widget, StreamsList, StreamCommand):
        """Restore the command for the current stream"""
        if StreamsList.get_active_text() in \
                self.default_streams_dict.keys():
            self.streams_dict[StreamsList.get_active_text()] = \
                self.default_streams_dict[StreamsList.get_active_text()]
        self.show_command(widget, StreamsList, StreamCommand)
        self.updateStreamsOnFile()

    def remove_current(self, widget, StreamsList):
        """Remove the current stream"""
        currentLabel = StreamsList.get_active_text()
        currentPos = sorted(self.streams_dict.keys())\
            .index(StreamsList.get_active_text())
        self.streams_dict.pop(currentLabel)
        StreamsList.remove(currentPos)
        StreamsList.set_active(0)
        self.reset_streams_submenu()
        self.update_recent_for_remove()
        self.updateStreamsOnFile()

    def export_streams(self, widget):
        """Export streams to file"""
        dialog = \
            Gtk.FileChooserDialog("Please choose a file", None,
                                  Gtk.FileChooserAction.SAVE,
                                  (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                   Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.OK:
            streamsf = open(dialog.get_filename(), 'w')
            for i in sorted(self.streams_dict.keys()):
                print(i + '\n' + self.streams_dict[i], file=streamsf)
            streamsf.close()
            dialog.destroy()

    def restore_defaults(self, widget, StreamsList):
        """Restore the default streams"""
        extras = []
        for i in range(len(self.streams_dict.keys())):
            if not (sorted(self.streams_dict.keys())[i] in
                    self.default_streams_dict.keys()):
                extras.append(i)

        for i in range(len(extras)):
            StreamsList.remove(extras[i]-i)

        extras = []
        for i in range(len(self.default_streams_dict.keys())):
            if not (sorted(self.default_streams_dict.keys())[i] in
                    self.streams_dict.keys()):
                extras.append(i)

        for i in range(len(extras)):
            StreamsList.insert_text(
                extras[i]+i,
                sorted(self.default_streams_dict.keys())[extras[i]])

        self.streams_dict = {}
        for i in self.default_streams_dict.keys():
            self.streams_dict[i] = self.default_streams_dict[i]

        self.reset_streams_submenu()
        self.updateStreamsOnFile()

    def show_command(self, widget, StreamsList, StreamCommand):
        """Show the streaming command for the currently selected key"""
        if StreamsList.get_active_text() is not None:
            StreamCommand.set_text(
                self.streams_dict[StreamsList.get_active_text()])

    def reset_streams_submenu(self):
        """Set the streams submenu to the current stream list"""
        # reset the submenu
        self.streams_menu_items = Gtk.Menu()
        self.streams_menu.set_submenu(self.streams_menu_items)
        # fill in the submenu items
        for i in sorted(self.streams_dict.keys()):
            stream_item = Gtk.MenuItem(i)
            stream_item.connect("activate", self.start_playback, i)
            stream_item.show()
            self.streams_menu_items.append(stream_item)

    def updateSettings(self):
        with open(self.settings_filename, 'w') as settings_file:
            print(self.recent_streams_num + '\n' + int(self.NotificationOn),
                  file=settings_file)

    def updateStreamsOnFile(self):
        streamsf = open(self.streams_filename, 'w')
        for i in sorted(self.streams_dict.keys()):
            print(i + '\n' + self.streams_dict[i], file=streamsf)
        streamsf.close()
