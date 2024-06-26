import random


def id_to_int(hospoda_id):
    # Konvertuje ID hospody na celé číslo, pokud je vstup float.
    return int(hospoda_id) if isinstance(hospoda_id, float) else hospoda_id


def krizeni(rodice):
    # Provede křížení dvou rodičů, aby vytvořil potomky.
    x = random.randint(0, len(rodice[0]) - 1)
    rodice[0][x:], rodice[1][x:] = rodice[1][x:], rodice[0][x:]
    return rodice


class GenetickyAlgoritmus:
    def __init__(self, hospoda, spravce_hospod, velikost_populace, generace, mutace_pravdepodobnost):
        # Inicializuje parametry genetického algoritmu.
        self.hospoda = hospoda
        self.spravce_hospod = spravce_hospod
        self.velikost_populace = velikost_populace
        self.generace = generace
        self.mutace_pravdepodobnost = mutace_pravdepodobnost

    def inicializace_populace(self):
        # Inicializuje počáteční populaci náhodnými cestami.
        populace = [list(range(1, len(self.spravce_hospod.hospody) + 1)) for _ in range(self.velikost_populace)]
        random.shuffle(populace)
        return populace

    def fitness(self, cesta):
        # Vypočítá fitness jedince jako 100 mínus celkovou vzdálenost.
        celkova_vzdalenost = self.spravce_hospod.vypocti_celkovou_vzdalenost(cesta)
        return 100 - celkova_vzdalenost

    def selekce(self, populace):
        # Provede selekci rodičů na základě jejich fitness.
        hodnoty_fitness = [self.fitness(cesta) for cesta in populace]
        total_fitness = sum(hodnoty_fitness)
        pravdepodobnosti = [fitness / total_fitness for fitness in hodnoty_fitness]
        rodic = random.choices(populace, weights=pravdepodobnosti, k=1)[0]
        index = populace.index(rodic)

        return rodic, index

    def mutace(self, rodice):
        # Provede mutaci na jedincích s danou pravděpodobností.
        for i in range(len(rodice)):
            if random.uniform(0.00, 1.00) < self.mutace_pravdepodobnost:
                index1, index2 = random.sample(range(len(rodice[i])), 2)
                rodice[i][index1], rodice[i][index2] = rodice[i][index2], rodice[i][index1]
        return rodice

    def odstran_duplikaty(self, po_krizeni):
        # Odstraní duplikáty z potomků po křížení.
        po_odstraneni = []

        for potomek in po_krizeni:
            duplicity = []
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
        # Najde jedince s nejnižší celkovou vzdáleností.
        minimum_hodnota = min(populace, key=self.spravce_hospod.vypocti_celkovou_vzdalenost)
        return minimum_hodnota

    def solve(self):
        # Spustí genetický algoritmus pro hledání nejlepší cesty.
        populace = self.inicializace_populace()

        for generace in range(self.generace):
            # Selece rodičů a provede křížení a mutaci.
            rodic1, index_krizeni1 = self.selekce(populace)
            rodic2, index_krizeni2 = self.selekce(populace)

            rodice = [rodic1, rodic2]

            # Křížení
            po_krizeni = krizeni(rodice)

            # Odstranění duplicit
            po_odstraneni_duplicit = self.odstran_duplikaty(po_krizeni)

            # Mutace
            po_mutaci = self.mutace(po_odstraneni_duplicit)

            # Zařazení zmutovaných cest
            populace[index_krizeni1] = po_mutaci[0]
            populace[index_krizeni2] = po_mutaci[1]

        # Nalezení nejkratší cesty
        nejlepsi_cesta = self.najdi_minimum(populace)
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Genetický algoritmus'
        )
