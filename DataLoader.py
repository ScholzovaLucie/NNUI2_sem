import pandas as pd


class DataLoader(object):
    def __init__(self, file_name):
        # Inicializace objektu pro načítání dat
        self.file_path = "files/" + file_name
        self.df = self.load_data_from_excel()

    def load_data_from_excel(self):
        # Načtení dat z Excel souboru
        return pd.read_excel(self.file_path)

    def format_data_for_algorithm(self):
        # Formátování dat pro použití v genetickém algoritmu
        pubs_data = []

        # Iterace přes řádky DataFrame
        for index, row in self.df.iterrows():
            if index == 0:
                continue

            # Extrahování informací o hospodě
            pub_id = row[0]
            pub_name = row[1]
            pub_coords = row[2]
            latitude, longitude = map(float, pub_coords.split(','))
            coordinate = [latitude, longitude]

            # Vytvoření slovníku s informacemi o hospodě
            pub_data = {
                'id': pub_id,
                "název": pub_name,
                "koordináty": coordinate,
            }

            # Přidání informací o hospodě do seznamu
            pubs_data.append(pub_data)

        return pubs_data
