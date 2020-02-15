# -*- coding: utf-8 -*-

from gi.repository import Gtk


class settings(object):
    def openSettings(self, widget):
        """Open the settings window"""
        window = Gtk.Window()
        window.present()
        window.set_title('Settings')
        window.set_resizable(False)
        window.connect("destroy", lambda w: w.destroy())

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       homogeneous=False, spacing=5)
        window.add(vbox)

        hboxNoti = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                           homogeneous=False, spacing=0)
        vbox.add(hboxNoti)

        PopupLabel = Gtk.Label('Show popups')
        hboxNoti.pack_start(PopupLabel, False, False, padding=5)

        PopupSwitch = Gtk.Switch()
        PopupSwitch.set_active(self.NotificationOn)
        PopupSwitch.connect('notify::active', self.notifications)
        hboxNoti.pack_start(PopupSwitch, False, False, padding=5)

        separator1 = Gtk.Separator()
        vbox.add(separator1)

        hboxRecentStreamsNum = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                                       homogeneous=False, spacing=0)
        vbox.add(hboxRecentStreamsNum)

        RecentStreamsNumLabel = Gtk.Label('Number of recent streams')
        RecentStreamsNumEntry = Gtk.Entry()
        RecentStreamsNumEntry.set_text(str(self.recent_streams_num))
        RecentStreamsNumEntry.set_width_chars(3)
        RecentStreamsNumButton = Gtk.Button('Set')
        RecentStreamsNumButton.connect('clicked', self.update_recent_num,
                                       RecentStreamsNumEntry)

        hboxRecentStreamsNum.pack_start(RecentStreamsNumLabel,
                                        False, False, padding=5)
        hboxRecentStreamsNum.pack_start(RecentStreamsNumEntry,
                                        False, False, padding=5)
        hboxRecentStreamsNum.pack_start(RecentStreamsNumButton,
                                        False, False, padding=5)

        separator2 = Gtk.Separator()
        vbox.add(separator2)

        hboxStreams = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                              homogeneous=False, spacing=0)
        vbox.add(hboxStreams)

        StreamsList = Gtk.ComboBoxText()
        for i in sorted(self.streams_dict.keys()):
            StreamsList.append_text(i)
        StreamsList.set_entry_text_column(0)

        StreamCommand = Gtk.Entry()
        StreamCommand.set_width_chars(50)
        StreamsList.connect('changed', self.show_command, StreamsList,
                            StreamCommand)
        StreamsList.set_active(0)

        hboxStreams.pack_start(StreamsList, False, False, padding=5)
        hboxStreams.pack_start(StreamCommand, False, False, padding=5)

        hboxStreamsEdit = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                                  homogeneous=False, spacing=0)
        vbox.add(hboxStreamsEdit)

        SaveStreamCommand = Gtk.Button('Update current')
        SaveStreamCommand.connect('clicked', self.update_current, StreamsList,
                                  StreamCommand)

        RestoreCurrent = Gtk.Button('Restore current')
        RestoreCurrent.connect('clicked', self.restore_current, StreamsList,
                               StreamCommand)

        RemoveCurrent = Gtk.Button('Remove current')
        RemoveCurrent.connect('clicked', self.remove_current, StreamsList)

        AddStream = Gtk.Button('Add stream...')
        AddStream.connect('clicked', self.add_stream_dialog, StreamsList)

        ExportStreams = Gtk.Button('Export...')
        ExportStreams.connect('clicked', self.export_streams)

        RestoreDefaults = Gtk.Button('Restore Defaults')
        RestoreDefaults.connect('clicked', self.restore_defaults, StreamsList)

        hboxStreamsEdit.pack_start(SaveStreamCommand, False, False, padding=5)
        hboxStreamsEdit.pack_start(RestoreCurrent, False, False, padding=5)
        hboxStreamsEdit.pack_start(RemoveCurrent, False, False, padding=5)
        hboxStreamsEdit.pack_start(AddStream, False, False, padding=5)
        hboxStreamsEdit.pack_start(ExportStreams, False, False, padding=5)
        hboxStreamsEdit.pack_start(RestoreDefaults, False, False, padding=5)

        window.show_all()
