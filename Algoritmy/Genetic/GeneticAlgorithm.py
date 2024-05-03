import random


def id_to_int(hospoda_id):
    # Funkce pro převod id na integer, pokud je id ve formátu float
    return int(hospoda_id) if isinstance(hospoda_id, float) else hospoda_id


class GenetickyAlgoritmus:
    def __init__(self, hospoda, spravce_hospod, velikost_populace, generace, mutace_pravdepodobnost):
        # Inicializace genetického algoritmu s parametry
        self.hospoda = hospoda
        self.spravce_hospod = spravce_hospod
        self.velikost_populace = velikost_populace
        self.generace = generace
        self.mutace_pravdepodobnost = mutace_pravdepodobnost

    def inicializace_populace(self):
        # Inicializace populace s náhodným pořadím návštěvy hospod
        populace = [list(range(1, len(self.spravce_hospod.hospody) + 1)) for _ in range(self.velikost_populace)]
        random.shuffle(populace)
        return populace

    def fitness(self, cesta):
        # Výpočet fitness hodnoty pro danou cestu
        celkova_vzdalenost = self.spravce_hospod.vypocti_celkovou_vzdalenost(cesta)
        return 100 - celkova_vzdalenost

    def selekce(self, populace):
        # Selekční metoda pro výběr rodičů
        hodnoty_fitness = [self.fitness(cesta) for cesta in populace]
        total_fitness = sum(hodnoty_fitness)
        pravdepodobnosti = [fitness / total_fitness for fitness in hodnoty_fitness]

        # Vybrání rodiče na základě pravděpodobnosti fitness
        rodic = random.choices(
            populace,
            weights=pravdepodobnosti,
            k=1,
        )[0]

        index = populace.index(rodic)

        return rodic, index

    def krizeni(self, rodice):
        # Křížení dvou rodičů na náhodném místě
        x = random.randint(0, len(rodice[0]) - 1)
        rodice[0][x:], rodice[1][x:] = rodice[1][x:], rodice[0][x:]
        return rodice

    def mutace(self, rodice):
        # Mutace cest podle dané pravděpodobnosti
        for i in range(len(rodice)):
            if random.uniform(0.00, 1.00) < self.mutace_pravdepodobnost:
                index1, index2 = random.sample(range(len(rodice[i])), 2)
                rodice[i][index1], rodice[i][index2] = rodice[i][index2], rodice[i][index1]
        return rodice

    def odstran_duplikaty(self, po_krizeni):
        # Odstranění duplicitních hodnot z potomků
        po_odstraneni = []
        for potomek in po_krizeni:
            duplicity = []
            chybejici = []

            int_ids = [id_to_int(hospoda['id']) for hospoda in self.spravce_hospod.hospody]
            duplicita_nalezena = []

            for id in potomek:
                pocet = potomek.count(id)
                if pocet > 1 and id not in duplicita_nalezena:
                    duplicita_nalezena.append(id)
                    duplicity.extend([id] * (pocet - 1))

            chybejici = [id for id in int_ids if potomek.count(id) < 1]

            for hodnota in duplicity:
                index = potomek.index(hodnota)
                potomek[index] = chybejici.pop(0)

            po_odstraneni.append(potomek)

        return po_odstraneni

    def najdi_minimum(self, populace):
        # Nalezení nejkratší cesty v populaci
        minimum_hodnota = min(populace, key=self.spravce_hospod.vypocti_celkovou_vzdalenost)
        return minimum_hodnota

    def solve(self):
        # Hlavní funkce pro spuštění genetického algoritmu
        populace = self.inicializace_populace()

        for generace in range(self.generace):
            # Selece rodičů
            rodic1, index_krizeni1 = self.selekce(populace)
            rodic2, index_krizeni2 = self.selekce(populace)

            rodice = [rodic1, rodic2]

            # Křížení
            po_krizeni = self.krizeni(rodice)

            # Odstranění duplicit
            po_odstraneni_duplicit = self.odstran_duplikaty(po_krizeni)

            # Mutace
            po_mutaci = self.mutace(po_odstraneni_duplicit)

            # Zařazení zmutovaných cest
            populace[index_krizeni1] = po_mutaci[0]
            populace[index_krizeni2] = po_mutaci[1]

        # Nalezení nejkratší cesty
        nejlepsi_cesta = self.najdi_minimum(populace)

        # Vrácení informací o nejlepší cestě a její celkové vzdálenosti
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Genetický algoritmus'
        )
