import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestComp = []
        self.graph = nx.Graph()
        self.idMap = {}
        self._bestLen = 0

    def getCountries(self):
        return DAO.getCountry()

    def getGraphDetails(self):
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."

    def get_nodes(self):
        return self.graph.nodes

    def buildGraph(self, year, country):
        self.graph.clear()
        nodes = DAO.getRetailers(country)
        self.graph.add_nodes_from(nodes)
        for node in self.graph.nodes:
            self.idMap[node.Retailer_name] = node
        edges = DAO.getEdges(year, country, self.idMap)
        for edge in edges:
            if self.graph.has_edge(edge.retailer1, edge.retailer2):
                pass
            else:
                self.graph.add_edge(edge.retailer1, edge.retailer2, weight=edge.weight)
        return True

    def analyze(self):
        result = []
        for node in self.graph.nodes:
            vicini = self.graph.neighbors(node)
            volume = 0
            for v in vicini:
                volume += self.graph[node][v]['weight']
            result.append((node, volume))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def getPath(self, maxLen):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestLen = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = []
        for node in self.graph.nodes:
            parziale.append(node)
            self._ricorsionev2(parziale, maxLen)
            parziale.pop()
        return self._bestComp

    def _ricorsionev2(self, parziale, maxLen):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale) - 1 == maxLen:
            if parziale[0] == parziale[-1]:
                if self._getScore(parziale) > self._bestLen:
                    self._bestComp = copy.deepcopy(parziale)
                    self._bestLen = self._getScore(parziale)
            return
        elif len(parziale) - 1 > maxLen:
            return
        # verifico se posso aggiungere un altro elemento
        last_node = parziale[-1]
        for a in self.graph.neighbors(last_node):
            if len(parziale) == maxLen:
                if a == parziale[0]:
                    parziale.append(a)
                    self._ricorsionev2(parziale, maxLen)
                    parziale.pop()
                elif parziale[0] not in self.graph.neighbors(last_node):
                    return
            if a not in parziale:
                parziale.append(a)
                self._ricorsionev2(parziale, maxLen)
                parziale.pop()

    def _getScore(self, nodes):
        score = 0
        for i in range(0, len(nodes) - 1):
            score += self.graph[nodes[i]][nodes[i + 1]]['weight']
        return score

    def getPathDetails(self):
        result = []
        for i in range(0, len(self._bestComp) - 1):
            result.append((self._bestComp[i], self._bestComp[i+1], self.graph[self._bestComp[i]][self._bestComp[i+1]]['weight']))
        return result
