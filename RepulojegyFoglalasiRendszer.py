from datetime import datetime, timedelta

class Jarat:
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    def __str__(self):
        return f"{self.jaratszam} - {self.celallomas} ({self.jegyar} Ft)"


class BelfoldiJarat(Jarat):
    """
    A feladatleírás nem tartalmazott specifikus funkciókat ehhez az osztályhoz
    (BelfoldiJarat: "Belföldi járatokra vonatkozó osztály, amelyek olcsóbbak és rövidebbek").
    Ez az osztály jelenleg csak a járatok kategorizálására szolgál,
    nincs szükség implementációra a követelmények teljesítéséhez.
    Az árak a rendszer inicializálásakor manuálisan lettek beállítva.
    """
    pass


class NemzetkoziJarat(Jarat):
    """
    A feladatleírás nem tartalmazott specifikus funkciókat ehhez az osztályhoz
    (NemzetkoziJarat: "Nemzetközi járatokra vonatkozó osztály, magasabb jegyárakkal").
    Ez az osztály jelenleg csak a járatok kategorizálására szolgál,
    nincs szükség implementációra a követelmények teljesítéséhez.
    Az árak a rendszer inicializálásakor manuálisan lettek beállítva.
    """
    pass


class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)

    def jarat_kereses(self, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None


class JegyFoglalas:
    kovetkezo_azonosito = 1

    def __init__(self, jarat, utas_neve, datum):
        self.foglalasi_azonosito = JegyFoglalas.kovetkezo_azonosito
        JegyFoglalas.kovetkezo_azonosito += 1
        self.jarat = jarat
        self.utas_neve = utas_neve
        self.datum = datum
        self.ar = jarat.jegyar

    def __str__(self):
        return (f"Foglalás: {self.foglalasi_azonosito}\n"
                f"Utas: {self.utas_neve}\n"
                f"Járat: {self.jarat}\n"
                f"Dátum: {self.datum.strftime('%Y-%m-%d %H:%M')}\n"
                f"Ár: {self.ar} Ft\n")


class FoglalasiRendszer:
    def __init__(self, legitarsasag):
        self.legitarsasag = legitarsasag
        self.foglalasok = []

    def foglalas(self, jaratszam, utas_neve, datum):
        jarat = self.legitarsasag.jarat_kereses(jaratszam)

        if not jarat:
            print("A megadott járat nem létezik!")
            return None

        if datum < datetime.now():
            print("Érvénytelen dátum!")
            return None

        foglalas = JegyFoglalas(jarat, utas_neve, datum)
        self.foglalasok.append(foglalas)
        print(f"Sikeres foglalás! Azonosító: {foglalas.foglalasi_azonosito}")
        return foglalas

    def foglalas_torles(self, azonosito):
        for foglalas in self.foglalasok:
            if foglalas.foglalasi_azonosito == azonosito:
                self.foglalasok.remove(foglalas)
                print(f"A {azonosito} azonosítójú foglalás törölve!")
                return True
        print("Nem található ilyen foglalás!")
        return False


def rendszer_inicializalas():
    legitarsasag = LegiTarsasag("Wizzair")

    # Járatok létrehozása
    jaratok = [
        BelfoldiJarat("BJ001", "Debrecen", 26000),
        BelfoldiJarat("BJ002", "Miskolc", 19000),
        NemzetkoziJarat("NJ001", "München", 125000)
    ]

    for jarat in jaratok:
        legitarsasag.jarat_hozzaadas(jarat)

    rendszer = FoglalasiRendszer(legitarsasag)

    # Kezdeti foglalások
    utasok = ["Hoppe Ralf", "Bella Katalin", "Benjamin Gotwald", "Kiss Szilárd", "Remek Elek", "Kozik Pawel"]

    for i, utas in enumerate(utasok):
        jarat = jaratok[i % len(jaratok)]
        datum = datetime.now() + timedelta(days=i + 1)
        rendszer.foglalas(jarat.jaratszam, utas, datum)

    return rendszer


def main():
    rendszer = rendszer_inicializalas()

    while True:
        print("\nRepülőjegy Foglalási Rendszer")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Válasszon műveletet (1-4): ")

        if valasztas == "1":
            jaratszam = input("Járatszám: ")
            utas_neve = input("Utas neve: ")
            napok = int(input("Hány nap múlva szeretne utazni? "))
            datum = datetime.now() + timedelta(days=napok)
            rendszer.foglalas(jaratszam, utas_neve, datum)

        elif valasztas == "2":
            azonosito = int(input("Foglalási azonosító: "))
            rendszer.foglalas_torles(azonosito)

        elif valasztas == "3":
            print("\nAktuális foglalások:")
            for foglalas in rendszer.foglalasok:
                print(foglalas)

        elif valasztas == "4":
            print("Viszontlátásra!")
            break

        else:
            print("Érvénytelen választás!")


if __name__ == "__main__":
    main()