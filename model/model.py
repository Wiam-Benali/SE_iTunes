import copy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.album = None
        self.collegamenti = None
        self.G = nx.Graph()

        self.soluzione_ottimale = []
        self.durata_ottimale = []

    def build_graph(self,d):
        self.G.clear()
        self.album = DAO.leggi_album(d)
        self.collegamenti = DAO.leggi_collegamenti(self.album,d)

        self.G.add_nodes_from(self.album.values())

        for arco in self.collegamenti:
            self.G.add_edge(arco.a1,arco.a2)

        return len(self.G.nodes),len(self.G.edges)

    def cerca_componenti_conesse(self,album):
        self._album_selezionato =  album
        self.connesse = list(nx.node_connected_component(self.G, album))
        return self.connesse


    def ricerca_set_album(self,d):

        for album in self.album:
            set_parziale = [ self.album[album]]
            durata = self.album[album].durata

            self.ricorsione(set_parziale,durata,d)
            print(self.soluzione_ottimale)
        return self.soluzione_ottimale

    def ricorsione(self,set_parziale,durata,d):
        if durata > d:
            return
        if self.soluzione_valida(set_parziale) and len(set_parziale) > len(self.soluzione_ottimale):
            if durata <= d:
                self.soluzione_ottimale = copy.deepcopy(set_parziale)
                self.durata_ottimale = copy.deepcopy(durata)



        ultimo_nodo = set_parziale[-1]
        for album in self.G.neighbors(ultimo_nodo):
            if album not in set_parziale:
                set_parziale.append(album)
                durata += album.durata
                self.ricorsione(set_parziale,durata,d)
                durata -= album.durata
                set_parziale.pop()






    def soluzione_valida(self,set_parziale):
        if self._album_selezionato not in set_parziale:
            return False


        for a in set_parziale:
            if a not in self.connesse:
                return False

        return True


