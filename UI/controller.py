import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            d = float(self._view.txt_durata.value)
            nodi,archi = self._model.build_graph(d)
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Grafo creato: {nodi} album, {archi} archi'))

            album = self._model.album.values()

            for a in album:
                self._view.dd_album.options.append(ft.dropdown.Option(key=a.id,
                                                     text=a.title))
            self._view.update()
        except ValueError:
            self._view.show_alert(f'Inserisci valore di durata valido')

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        album_id = e.control.value
        self._selected_album = self._model.album[int(album_id)]

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if not self._selected_album:
            self._view.show_alert("Selezionare un album")
            return
        else:
            print(self._selected_album)
            connesse = self._model.cerca_componenti_conesse(self._selected_album)
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione componente {len(connesse)}'))
            somma = 0
            for album in connesse:
                somma += album.durata
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Durata totale {somma:.2f}'))

            self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        try:
            print('ho')
            d = float(self._view.txt_durata_totale.value)
            set = self._model.ricerca_set_album(d)
            print('hi')
            for i in set:
                print(set)
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f'{i}'))
            self._view.update()
        except ValueError:
            self._view.show_alert(f'Inserisci valore di durata valido')


