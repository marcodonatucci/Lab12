import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = self._model.getCountries()
        for country in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(str(country)))
        self._view.update_page()
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._view.ddyear.value is None or self._view.ddcountry.value is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci una nazione e un anno!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(self._view.ddyear.value, self._view.ddcountry.value)
        if flag:
            self._view.txt_result.controls.append(ft.Text(self._model.getGraphDetails()))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return



    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txtOut2.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        result = self._model.analyze()
        if len(result) == 0:
            self._view.txtOut2.controls.append(ft.Text("Nessun risultato trovato!", color='red'))
            self._view.update_page()
            return
        for r in result:
            self._view.txtOut2.controls.append(ft.Text(f"{r[0]} --> {r[1]}"))
        self._view.update_page()



    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txtOut3.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        d = self._view.txtN.value
        if d is None or d == '':
            self._view.txtOut3.controls.append(ft.Text("Inserire una soglia massima!", color='red'))
            self._view.update_page()
            return
        try:
            d = int(d)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Inserisci una soglia in formato numerico!", color='red'))
            self._view.update_page()
            return
        if d < 2:
            self._view.txtOut3.controls.append(ft.Text("Inserisci una soglia maggiore di 2!", color='red'))
            self._view.update_page()
            return
        percorso = self._model.getPath(d)
        if percorso:
            self._view.txtOut3.controls.append(ft.Text(f"Somma totale dei pesi: {self._model._bestLen}"))
            for c in self._model.getPathDetails():
                self._view.txtOut3.controls.append(ft.Text(f"{c[0]} --> {c[1]}: {c[2]}"))
            self._view.update_page()
            return
        else:
            self._view.txtOut3.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return

