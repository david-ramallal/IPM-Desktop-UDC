#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import gettext

_ = gettext.gettext
N_ = gettext.ngettext


class View:
    run_on_main_thread = GLib.idle_add

    WINDOW_PADDING: int = 24

    win: Gtk.ApplicationWindow = None
    error_dialog: Gtk.Dialog = None
    current_filter_language: Gtk.TreeModelFilter = None
    error_label: Gtk.Label = None
    search_entry: Gtk.SearchEntry = None
    spinner: Gtk.Spinner = None
    historic_list: Gtk.ListBox = None
    list_store: Gtk.ListStore = None

    def build(self, app: Gtk.Application, presenter) -> None:
        self.win = Gtk.ApplicationWindow(title=_("Cheat.sh Desktop"))
        app.add_window(self.win)
        self.win.set_child(self.creator(presenter))
        self.win.present()

    def creator(self, presenter) -> Gtk.Widget:
        # grid general
        app_grid = Gtk.Grid(
            margin_top=View.WINDOW_PADDING,
            margin_end=View.WINDOW_PADDING,
            margin_bottom=View.WINDOW_PADDING,
            margin_start=View.WINDOW_PADDING)
        # caja derecha
        right_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            spacing=12,
        )
        # caja izquierda
        left_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            hexpand=True,
            spacing=12,
            margin_end=View.WINDOW_PADDING,
        )
        # caja de búsqueda (spinner y entrada de búsqueda)
        search_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=5
        )
        # caja comandos
        command_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            spacing=12
        )

        error_dialog = Gtk.Dialog(title="Cheat.sh",  transient_for=self.win, hide_on_close=True)
        error_dialog.set_default_size(400, 25)

        error_label = Gtk.Label()
        error_label.get_style_context().add_class("error")

        error_box = error_dialog.get_content_area()
        error_box.append(error_label)

        search_entry = Gtk.SearchEntry(placeholder_text=_("Search Command..."), width_chars=80)
        spinner = Gtk.Spinner()
        search_box.append(search_entry)
        search_box.append(spinner)

        search_entry.connect("activate", presenter.on_search_command)

        # lista de históricos
        historic_list = Gtk.ListBox(vexpand=True)
        historic_label = Gtk.Label(label=_("Last searches"))

        scroll_historic = Gtk.ScrolledWindow()
        scroll_historic.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_historic.set_child(historic_list)

        # lista de resultados
        list_store = Gtk.ListStore(str, str)

        language_filter = list_store.filter_new()
        language_filter.set_visible_func(self.language_filter_func)

        tree = Gtk.TreeView(model=language_filter, vexpand=True)

        renderer_text = Gtk.CellRendererText(wrap_width=100)
        command_column = Gtk.TreeViewColumn(_("Command"), renderer_text, text=0)
        command_column.set_min_width(300)
        description_column = Gtk.TreeViewColumn(_("Description"), renderer_text, text=1)

        tree.append_column(command_column)
        tree.append_column(description_column)

        scroll_tree = Gtk.ScrolledWindow()
        scroll_tree.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_tree.set_child(tree)

        # auxiliar function 
        def aux(self, lst):
            text = lst.get_child().get_text()
            presenter.on_historic_command(text)

        historic_list.connect("row-activated", aux)

        command_box.append(scroll_tree)

        # construimos la rightbox
        right_box.append(historic_label)
        right_box.append(scroll_historic)

        # construimos la leftbox
        left_box.append(search_box)
        left_box.append(command_box)

        # construimos el grid
        app_grid.attach(left_box, 0, 0, 2, 1)
        app_grid.attach(right_box, 4, 0, 1, 1)

        self.error_label = error_label
        self.error_dialog = error_dialog
        self.search_entry = search_entry
        self.spinner = spinner
        self.historic_list = historic_list
        self.list_store = list_store
        self.current_filter_language = language_filter

        return app_grid

    def language_filter_func(self, model, iterator, data):
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iterator][0].startswith(self.current_filter_language)

    def spinner_start(self):
        self.spinner.start()

    def spinner_stop(self):
        self.spinner.stop()

    def update_view(self, command: str, list_command: list):
        label_command = Gtk.Label(label=command)
        self.historic_list.insert(label_command, -1)  # Añade el comando al histórico
        self.search_entry.set_text("")  # Pone en blanco la barra de búsqueda
        self.current_filter_language = command
        self.list_store.clear()
        if len(list_command) == 0:
            self.error_label.set_text(_("Error: Command not found"))
            self.error_dialog.show()
            self.error_label.show()
        else:
            for a_tuple in list_command:
                self.list_store.append([a_tuple[0], a_tuple[1]])
            self.error_label.hide()
            self.error_dialog.hide() 

    def update_view_error(self, command: str):
        label_command = Gtk.Label(label=command)
        self.historic_list.insert(label_command, -1)  # Añade el comando al histórico
        self.search_entry.set_text("")  # Pone en blanco la barra de búsqueda
        self.list_store.clear()

        self.error_label.set_text(_("Error: Search not done"))
        self.error_dialog.show()
        self.error_label.show()

