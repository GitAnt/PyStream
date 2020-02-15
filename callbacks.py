# -*- coding: utf-8 -*-

from gi.repository import Gtk
from os import setsid, killpg
from subprocess import Popen
from signal import SIGTERM


class callbacks(object):

    # Define the methods to start a streaming, stop the streaming,
    # update the recent streams list, edit the streams database and
    # quit the indicator
    def start_playback(self, widget, pos=None):
        """Start the required stream stopping the stream that's
        playing, if any"""
        if len(self.recent_streams) > 0 and \
                pos != self.recent_streams[0] or \
                self.player_proc is None or \
                self.player_proc.poll() is not None:
            self.stop_playback(widget)
            self.ind.set_icon(self.cwd+"/icons/pyradio_invert.svg")
            self.player_proc = Popen(self.streams_dict[pos],
                                     shell=True,
                                     preexec_fn=setsid)
            self.current.set_label("Playing: " + pos)
            self.update_recent(pos)
            if self.NotificationOn:
                self.not_bubble.update('PyRadio',
                                       'Playing %s' % pos,
                                       self.cwd+"/icons/pyradio_invert.svg")
                self.not_bubble.show()
        else:
            if self.NotificationOn:
                self.not_bubble.update('PyRadio',
                                       '%s is already playing' % pos,
                                       self.cwd+"/icons/pyradio_invert.svg")
                self.not_bubble.show()

    def stop_playback(self, widget):
        """Stop the current stream"""
        if self.player_proc is not None:
            if self.player_proc.poll() is None:
                killpg(self.player_proc.pid, SIGTERM)
                self.player_proc = None
                if self.NotificationOn:
                    self.not_bubble.update('PyRadio', 'Stopping playback',
                                           self.cwd+"/icons/pyradio.svg")
                    self.not_bubble.show()
            else:
                self.player_proc = None
                if self.NotificationOn:
                    self.not_bubble.update('PyRadio',
                                           'Playback already stopped',
                                           self.cwd+"/icons/pyradio.svg")
                    self.not_bubble.show()
            self.ind.set_icon(self.cwd+"/icons/pyradio.svg")
            self.current.set_label("No stream playing")

    def update_recent(self, pos=None):
        """Update the list of recent streams"""
        if (pos in self.recent_streams):
            index = self.recent_streams.index(pos)
            self.recent_streams.pop(index)
        self.recent_streams.insert(0, pos)

        while len(self.recent_streams) > self.recent_streams_num:
            self.recent_streams.pop(-1)
        self.update_recent_menu()
        self.updateRecentOnFile()

    def update_recent_for_remove(self):
        """Update the list of recent streams after a stream has been removed"""
        for i in self.recent_streams:
            if i not in self.streams_dict.keys():
                index = self.recent_streams.index(i)
                self.recent_streams.pop(index)
        self.update_recent_menu()
        self.updateRecentOnFile()

    def update_recent_menu(self):
        """Update the recent streams menu"""
        self.recent_streams_menu_items = Gtk.Menu()
        self.recent.set_submenu(self.recent_streams_menu_items)
        for i in self.recent_streams:
            stream_item = Gtk.MenuItem(i)
            stream_item.connect("activate", self.start_playback, i)
            stream_item.show()
            self.recent_streams_menu_items.append(stream_item)

    def updateRecentOnFile(self):
        with open(self.recent_streams_filename, 'w') as recent_streams_file:
            for i in self.recent_streams:
                print(i, file=recent_streams_file)

    def quit(self, widget):
        """Close applet"""
        if self.player_proc is not None:
            self.stop_playback(widget)

        Gtk.main_quit()
