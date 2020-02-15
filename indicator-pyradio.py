#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3 as AppIndicator, Notify
from gi.repository.Gdk import color_parse
from os import path

from callbacks import callbacks
from settings import settings
from settingsCallbacks import settingsCallbacks
from addStream import addStream


class PyRadio(callbacks, settings, settingsCallbacks, addStream):
    """A simple stream player"""
    def __init__(self):
        self.cwd = path.dirname(path.realpath(__file__))
        self.ind = AppIndicator.Indicator.new(
            "PyRadio indicator",
            self.cwd+"/icons/pyradio.svg",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)

        self.backup_streams_filename = \
            self.cwd + "/" + "streams_list_backup.txt"
        self.streams_filename = self.cwd + "/" + "streams_list.txt"
        self.settings_filename = self.cwd + "/" + "settings.txt"
        self.default_streams_dict = {}
        self.streams_dict = {}
        self.player_proc = None
        self.recent_streams_filename = path.join(self.cwd,
                                                 "recent_streams_list.txt")
        self.recent_streams = []
        self.recent_streams_num = 0
        self.error_color = color_parse('#FA0223')

        with open(self.backup_streams_filename, 'r') as streams_file:
            streams = streams_file.readlines()
        for i in range(len(streams)//2):
            self.default_streams_dict[streams[2*i].strip()] = \
                streams[2*i+1].strip()

        with open(self.streams_filename, 'r') as streams_file:
            streams = streams_file.readlines()
        for i in range(len(streams)//2):
            self.streams_dict[streams[2*i].strip()] = streams[2*i+1].strip()

        self.NotificationOn = False
        Notify.init('PyRadio')
        self.not_bubble = Notify.Notification.new('', '', None)

        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        # Define a new menubar item "Streams"
        self.streams_menu = Gtk.MenuItem("Streams")
        self.streams_menu.show()
        self.menu.append(self.streams_menu)
        self.reset_streams_submenu()

        # Define a new menubar item "Recent streams"
        self.recent = Gtk.MenuItem("Recently played")
        self.recent.show()
        self.menu.append(self.recent)
        # Define a menu and some of its items and add it to the
        # "Recent streams" menubar element
        self.recent_streams_menu_items = Gtk.Menu()
        self.recent.set_submenu(self.recent_streams_menu_items)
        # read the recent stream list from file and populate the menu
        streams_file = open(self.recent_streams_filename, 'r')
        self.recent_streams = streams_file.readlines()
        streams_file.close()
        for i in range(len(self.recent_streams)):
            self.recent_streams[i] = self.recent_streams[i].strip()
        for i in self.recent_streams:
            stream_item = Gtk.MenuItem(i)
            stream_item.connect("activate", self.start_playback, i)
            stream_item.show()
            self.recent_streams_menu_items.append(stream_item)

        # Read in the settings
        settings_file = open(self.settings_filename, 'r')
        settings = settings_file.readlines()
        settings_file.close()
        self.recent_streams_num = int(settings[0].strip())
        self.NotificationOn = bool(int(settings[1].strip()))

        # Define a main menu item to stop the streaming
        self.stop = Gtk.MenuItem("Stop streaming")
        self.stop.connect("activate", self.stop_playback)
        self.stop.show()
        self.menu.append(self.stop)

        # Define a main menu item to display the currently playing stream
        self.current = Gtk.MenuItem("No stream playing")
        self.current.show()
        self.menu.append(self.current)

        # Define a main menu item to stop the streaming
        self.prefs = Gtk.MenuItem("Open settings...")
        self.prefs.connect("activate", self.openSettings)
        self.prefs.show()
        self.menu.append(self.prefs)

        # Define a main menu item to close the indicator
        self.quit_item = Gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

        # Attach the menu to the indicator
        self.ind.set_menu(self.menu)

    def main(self):
        """Start the Gtk loop"""
        Gtk.main()

if __name__ == "__main__":
    PyRadio().main()
