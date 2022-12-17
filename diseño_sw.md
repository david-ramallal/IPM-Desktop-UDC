# Diseño software

<!-- ## Notas para el desarrollo de este documento
En este fichero debeis documentar el diseño software de la práctica.

> :warning: El diseño en un elemento "vivo". No olvideis actualizarlo
> a medida que cambia durante la realización de la práctica.

> :warning: Recordad que el diseño debe separar _vista_ y
> _estado/modelo_.
	 

El lenguaje de modelado es UML y debeis usar Mermaid para incluir los
diagramas dentro de este documento. Por ejemplo:

-->
### Diagrama estático
```mermaid
classDiagram
  class CheatEntry{
  str : mark
  str : description
  str : commands
  str : tags
  __str__(self)
  }
  class Model {
  str : command
  set_command(self, command: str)
  get_command(self)
  obtain_command(self, command: str)
	}
  Model ..> CheatEntry : << uses >>
  class Presenter {
  __init__(self)
  run(self)
  on_activate(self, app: Gtk.Application))
  on_search_command(self, searchentry: str)
  on_historic_command(self, text: str)
  create_thread(self, text: str)
  update_commands(self, text: str)
  }
  Presenter ..> View : << uses >>
  Presenter ..> Model : << uses >>
	class View {
  Gtk.TreeModelFilter : current_filter_language
  Gtk.Label : error_label
  Gtk.SearchEntry : search_entry
  Gtk.Spinner : spinner
  Gtk.ListBox : historic_list
  Gtk.ListStore : list_store
  int : iteration
  build(self, app: Gtk.Application, presenter)
  creator(self, presenter)
  language_filter_func(self, model, iterator, data)
  spinner_start(self)
  spinner_stop(self)
  update_view(self, command: str, list_store_command: list)
  update_view_error(self, command: str)
	}
  View ..> Presenter : << uses >>

```
### Diagrama secuencia
``` mermaid
sequenceDiagram
    participant View
    participant Presenter
    participant Model
    
    View -->> Presenter : connect(activate, presenter.on_search_command)
    Presenter -->> Presenter : on_historic_command(self, text)
    Presenter -->> Presenter : create_thread(self, text)
    Presenter -->> Presenter : update_commands(self, text)
    Presenter -->> View : start_thread()
    Presenter -->> Model : set_command(searchentry.get_text())
    Model -->> Presenter : return()
    Presenter -->> Model : obtain_command(text)
    Model -->> Presenter : return()
    Presenter -->> View : stop_thread()
    alt error
      Presenter -->> Model : get_command()
      Model -->> Presenter : command
      Presenter -->> View : update_view_error(command)
    else not_error
      Presenter -->> Model : get_command()
      Model -->> Presenter : command
      Presenter -->> Model : obtain_command()
      Model -->> Presenter : list_command
      Presenter -->> View : update_view(command, list_command)
    end
```
