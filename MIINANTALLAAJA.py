"""Tämän miinantallaajan ovat tehneet yhteistyössä Väinö Juntura
sekä Juuso Säärelä.
"""



import sys
import os
import time
import random

def alkuvalikko():
    """
    Alkuvalikko:
    Suorittaa halutun toiminnon kyselemisen käyttäjältä.
    """
    while True:
        print("\nMiinantallaaja")
        print("\n[U]usi peli")
        print("[L]opeta")
        print("[T]ilastot\n")
        valinta = input("Valitse: ")
        valinta = valinta.lower()
        if valinta == "u" or valinta == "uusi peli":
            peli_paafunktio()
            break
        if valinta == "l" or valinta == "lopeta":
            os._exit(1)
        if valinta == "t" or valinta == "tilastot":
            print("\n")
            lue_tilastot("tilastot.txt")
        else:
            print("Valintaa ei ole olemassa!")






def peli_paafunktio():
    """
    Pelipääfunktio:
    Pyörittää peli looppia.
    """
    kentta_korkeus, kentta_leveys, miina_lkm = kysy_kentta()
    kentta, jaljella = luo_kentta(kentta_korkeus, kentta_leveys, miina_lkm)

    alkuaika = time.time()
    siirrot = 0

    while True:
        tulosta_kentta(kentta)
        x_koordinaatti, y_koordinaatti = kysy_koordinaatit(kentta_korkeus, kentta_leveys)

        siirrot += 1

        laske_miinat(x_koordinaatti, y_koordinaatti, jaljella, kentta)
        temp = tulvataytto(kentta, x_koordinaatti, y_koordinaatti, jaljella)


        if sum(x.count("o") for x in kentta) == miina_lkm:

            tulosta_kentta(kentta)
            print("Voitit pelin!")
            tulos = "Menestys!"

            kokoa_tilastot(siirrot, alkuaika, miina_lkm, kentta_korkeus, kentta_leveys, tulos)


            while True:
                valinta = input("Haluatko pelata uudestaan? K/E: ")

                if valinta.lower() == "k":
                    peli_paafunktio()
                    break
                elif valinta.lower() == "e":
                    alkuvalikko()
                    break
                else:
                    print("Väärä valinta!")
                    continue

        if (x_koordinaatti, y_koordinaatti) not in jaljella:
            tulosta_kentta(kentta)

            print("\nHävisit pelin!\n")
            tulos = "Tappio!"

            kokoa_tilastot(siirrot, alkuaika, miina_lkm, kentta_korkeus, kentta_leveys, tulos)
            while True:
                valinta = input("Haluatko pelata uudestaan? K/E: ")

                if valinta.lower() == "k":
                    peli_paafunktio()
                    break
                elif valinta.lower() == "e":
                    alkuvalikko()
                    break
                else:
                    print("Väärä valinta!")
                    continue

def kysy_kentta():
    """
    Kysy kenttä:
    Tenttaa käyttäjältä kentän ominaisuudet oikeassa muodossa.
    """
    try:
        while True:
            kentta_leveys = input("Anna kentän leveys tai lopeta tyhjällä: ")
            if not kentta_leveys:
                os._exit(1)
            else:
                try:
                    kentta_leveys = int(kentta_leveys)
                    if kentta_leveys <= 1:
                        raise TypeError
                except ValueError:
                    print("Anna leveys kokonaislukuna!")
                    continue
                except TypeError:
                    print("Syötit liian pienen leveyden!")
                    continue
                else:
                    break
        while True:
            kentta_korkeus = input("Anna kentän korkeus tai lopeta tyhjällä: ")
            if not kentta_korkeus:
                os._exit(1)
            else:
                try:
                    kentta_korkeus = int(kentta_korkeus)
                    if kentta_korkeus <= 1:
                        raise TypeError
                except ValueError:
                    print("Anna korkeus kokonaislukuna!")
                    continue
                except TypeError:
                    print("Syötit liian pienen korkeuden!")
                    continue
                else:
                    break

        while True:
            miina_lkm = input("Anna miinojen lukumäärä tai lopeta tyhjällä: ")
            if not miina_lkm:
                os._exit(1)
            else:
                try:
                    miina_lkm = int(miina_lkm)
                    if miina_lkm <= 0:
                        raise TypeError
                    elif miina_lkm > (kentta_korkeus * kentta_leveys - 1):
                        raise NameError
                except ValueError:
                    print("Anna miinojen lukumäärä kokonaislukuna!")
                    continue
                except TypeError:
                    print("Syötit liian pienen miinojen lukumäärän!")
                    continue
                except NameError:
                    print("Syötit liian suuren miinojen lukumäärän!")
                    continue
                else:
                    break

    except None:
        pass
    else:
        return kentta_korkeus, kentta_leveys, miina_lkm


def luo_kentta(kentta_korkeus, kentta_leveys, miina_lkm):
    """
    Luo kenttä:
    Luo pelikentän.
    """
    kentta = []
    jaljella = []
    miinat = []
    for lista in range(kentta_korkeus):
        kentta.append([])
        for alkio in range(kentta_leveys):
            kentta[-1].append("o")

    for x in range(kentta_leveys):
        for y in range(kentta_korkeus):
            jaljella.append((x, y))

    for miinat in range(miina_lkm):
        miinoita_satunnainen(kentta, jaljella)

    return kentta, jaljella



def tulosta_kentta(kentta):
    """
    Tulosta kenttä:
    Tulostaa kentän.
    """
    print("  ", end="")

    for i in range(len(kentta[0])):
        print(" {:0>2d}".format(i), end="")

    print()

    for index, rivi in enumerate(kentta):
        print("{:0>2d}  ".format(index), end="")
        print("  ".join(rivi))


def miinoita_satunnainen(kentta, jaljella):
    """
    Miinoita satunnainen:
    Miinoittaa kentän satunnaisesti.
    """

    miina_koordinaatti = random.choice(jaljella)
    jaljella.remove(miina_koordinaatti)
    x, y = miina_koordinaatti


    #kentta[y][x] = "x"
    return x,y


def kysy_koordinaatit(kentta_korkeus, kentta_leveys):
    """
    Kysy koordinaatit:
    Tenttaa määrätietoisesti käyttäjältä avattavia koordinaatteja.
    """
    while True:
        pisteet = input("Anna koordinaatit pilkulla erotettuna tai lopeta tyhjällä: ")
        if not pisteet:
            os._exit(1)
        try:
            jono = pisteet.split(",")
            x_koordinaatti = int(jono[0])
            y_koordinaatti = int(jono[1])
        except ValueError:
            print("Anna koordinaatit kokonaislukuina")
        except IndexError:
            print("Anna kaksi koordinaattia pilkulla erotettuna")
        else:
            if x_koordinaatti > (kentta_leveys - 1) or y_koordinaatti > (kentta_korkeus - 1) or x_koordinaatti < 0 or y_koordinaatti < 0:
                print("Koordinaatit ovat ruudukon ulkopuolella")
            else:
                return x_koordinaatti, y_koordinaatti


def tarkista_koordinaatit(planeetta, x_0, y_0):
    """
    Tarkista koordinaatit:
    Tarkistaa ovatko annetut koordinaatit kentällä.
    """
    if x_0 >= len(planeetta[0]) or y_0 >= len(planeetta) or x_0 < 0 or y_0 <0:
        return False
    else:
        return True

def tarkista_planeetasta(planeetta, x ,y):
    """

    """
    korkeus = len(planeetta)
    leveys = len(planeetta[0])
    if x < 0 or y < 0 or x > leveys - 1 or y > korkeus -  1:
        return False
    else:
        return True


def tulvataytto(planeetta, x_0, y_0, jaljella):
    """
    Tulvatäyttö:
    Suorittaa tyhjien ruutujen avaamisen.
    """
    koordinaattilista = []
    temp = []
    if (x_0, y_0) in jaljella:
        if tarkista_koordinaatit(planeetta, x_0, y_0) == True and planeetta[y_0][x_0] == "o":
            koordinaattilista.append((x_0, y_0))
    while len(koordinaattilista) > 0:
        x, y = koordinaattilista.pop()
        #print(x,y)

        if (x, y) not in jaljella:
            continue
        miinat = laske_miinat(x, y, jaljella, planeetta)
        if miinat != " ":
            planeetta[y][x] = str(miinat)
            continue
        planeetta[y][x] = str(miinat)

        if tarkista_planeetasta(planeetta, x, y + 1) == True and planeetta[y + 1][x] == "o" and (x, y) in jaljella:
            koordinaattilista.append( (x, y + 1) )
        if tarkista_planeetasta(planeetta, x, y - 1) == True and planeetta[y - 1][x] == "o" and (x, y) in jaljella:
            koordinaattilista.append( (x, y - 1) )
        if tarkista_planeetasta(planeetta, x + 1, y) == True and planeetta[y][x + 1] == "o" and (x, y) in jaljella:
            koordinaattilista.append( (x + 1, y) )
        if tarkista_planeetasta(planeetta, x - 1, y) == True and planeetta[y][x - 1] == "o" and (x, y) in jaljella:
            koordinaattilista.append( (x - 1, y) )

    return

def laske_miinat(x, y, jaljella, planeetta):
    """
    Laske miinat:
    Laskee ympärillä olevat miinat.
    """

    miinat = 0
    if tarkista_planeetasta(planeetta, x - 1, y) == True and (x -1, y) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x + 1, y) == True and (x + 1, y) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x, y + 1) == True and (x, y + 1) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x, y - 1) == True and (x, y - 1) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x + 1, y + 1) == True and (x + 1, y + 1) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x - 1, y - 1) == True and (x - 1, y - 1) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x - 1, y + 1) == True and (x - 1, y + 1) not in jaljella:
        miinat += 1
    if tarkista_planeetasta(planeetta, x + 1, y - 1) == True and (x + 1, y - 1) not in jaljella:
        miinat += 1

    if miinat == 0:
        miinat = " "

    return miinat


def kokoa_tilastot(siirrot, alkuaika, miina_lkm, kentta_korkeus, kentta_leveys, tulos):
    """
    Kokoa tilastot:
    Kerää pelitilastot tallentamista varten.
    """
    ajankohta = time.strftime("%X, %d.%m.%Y")
    kesto = time.time() - alkuaika
    kesto_minuutteina = round((kesto / 60))
    sekunnit = round(kesto % 60)


    merkkijono = "Alkuaika: {alkuaika}\nKesto: {kesto_minuutteina} min {sekunnit} sek\nSiirrot: {siirrot}\nMiinojen lukumäärä: {miina_lkm}\nKentän koko: {kentta_leveys}x{kentta_korkeus}\nTulos: {tulos}\n\n".format(alkuaika=ajankohta, kesto_minuutteina=kesto_minuutteina, sekunnit=sekunnit, siirrot=siirrot, miina_lkm=miina_lkm, kentta_leveys=kentta_leveys, kentta_korkeus=kentta_korkeus, tulos=tulos)
    print(merkkijono)
    return kirjoita_tiedostoon("tilastot.txt", merkkijono)


def kirjoita_tiedostoon(tiedosto, merkkijono):
    """
    Kirjoita tiedostoon:
    Kirjoittaa annetun sisällön määrätyn nimiseen tiedostoon ja sulkee tiedoston.
    """
    with open (tiedosto, "a") as kohde:
        kohde.write(merkkijono)

def lue_tilastot(tiedosto):
    """
    Lue tilastot:
    Avaa tilastot luettavaksi.
    """
    with open (tiedosto,"r") as kohde:
        print(kohde.read())



if __name__ == "__main__":
    alkuvalikko()
