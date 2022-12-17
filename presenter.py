#!/usr/bin/env python3
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from model import Model
from view import View
from threading import Thread


class Presenter:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self) -> None:
        app = Gtk.Application()
        app.connect('activate', self.on_activate)
        app.run(None)

    def on_activate(self, app: Gtk.Application) -> None:
        self.view.build(app, self)

    def on_search_command(self, searchentry) -> None:
        text = searchentry.get_text()
        self.on_historic_command(text)

    def on_historic_command(self, text) -> None:
        if text != "":
            self.model.set_command(text)
            self.create_thread(text)

    def create_thread(self, text):
        # iniciar thread
        t = Thread(target=self.update_commands, args=(text,))
        t.start()

    def update_commands(self, text) -> None:
        View.run_on_main_thread(self.view.spinner_start)

        self.model.set_command(text)
        command = self.model.get_command()
        try:
            lst = self.model.obtain_command(text)
            View.run_on_main_thread(self.view.spinner_stop)
            View.run_on_main_thread(self.view.update_view, command, lst)

        except OSError:
            View.run_on_main_thread(self.view.spinner_stop)
            View.run_on_main_thread(self.view.update_view_error, command)


