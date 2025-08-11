import json

with open("codici_catastali.json", "r", encoding="utf-8") as f:
    codici = json.load(f)

class CodiceCatastaleNonTrovato(Exception):
    pass

def get_codice_catastale(nome_comune, provincia, codici):
    nome_comune = nome_comune.strip().upper()
    provincia = provincia.strip().upper()
    nome = f"{nome_comune} ({provincia})"

    if nome in codici:
        return codici[nome]
    else:
        raise CodiceCatastaleNonTrovato(f"Codice catastale per '{nome_comune} ({provincia})' non trovato.")
        return f"Codice catastale per '{nome}' non trovato."
    
    

def calcola_cognome_cf(cognome):
    vocali = "AEIOU"
    cognome = cognome.upper()

    # Estraiamo consonanti e vocali
    consonanti = [c for c in cognome if c.isalpha() and c not in vocali]

    vocali_trovate = [c for c in cognome if c.isalpha() and c in vocali]

    # Costruiamo la stringa iniziale con consonanti + vocali
    cf = "".join(consonanti) + "".join(vocali_trovate)

    # Completamento con 'X' se meno di 3 caratteri
    cf = (cf + "XXX")[:3]

    return cf

def calcola_nome_cf(nome):
    vocali = "AEIOU"
    nome = nome.upper()

    consonanti = [c for c in nome if c.isalpha() and c not in vocali]
    vocali_trovate = [c for c in nome if c.isalpha() and c in vocali]

    if len(consonanti) >= 4:
        # prendiamo 1°, 3°, 4° consonante
        cf = consonanti[0] + consonanti[2] + consonanti[3]
    else:
        # prendi tutte le consonanti e poi vocali per arrivare a 3
        cf = "".join(consonanti) + "".join(vocali_trovate)
        cf = (cf + "XXX")[:3]

    return cf

def calcola_data_cf(sesso, giorno, mese, anno):
    # Dizionario mese -> lettera
    mese_lettera = {
        1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "H",
        7: "L", 8: "M", 9: "P", 10: "R", 11: "S", 12: "T"
    }
    
    anno_str = str(anno)[-2:]  # ultime 2 cifre anno
    mese_str = mese_lettera.get(mese, "?")  # ? se mese sbagliato
    
    if sesso.lower() in ["f", "femmina", "female"]:
        giorno += 40  # aggiungi 40 se femmina
    
    giorno_str = f"{giorno:02d}"  # formato 2 cifre (es. 1 -> "01")

    return anno_str + mese_str + giorno_str

def calcola_carattere_controllo(cf15):
    valori_dispari = {
        '0':1, '1':0, '2':5, '3':7, '4':9, '5':13, '6':15, '7':17, '8':19, '9':21,
        'A':1, 'B':0, 'C':5, 'D':7, 'E':9, 'F':13, 'G':15, 'H':17, 'I':19, 'J':21,
        'K':2, 'L':4, 'M':18, 'N':20, 'O':11, 'P':3, 'Q':6, 'R':8, 'S':12, 'T':14,
        'U':16, 'V':10, 'W':22, 'X':25, 'Y':24, 'Z':23
    }
    valori_pari = {
        '0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
        'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9,
        'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19,
        'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25
    }
    lettere_controllo = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    somma = 0
    for i, char in enumerate(cf15):
        if (i + 1) % 2 != 0:  # posizione dispari
            somma += valori_dispari[char]
        else:  # posizione pari
            somma += valori_pari[char]

    return lettere_controllo[somma % 26]


while True:
    cognome = input("Inserisci il cognome ")
    cognomeCF = calcola_cognome_cf(cognome)
    #print(cognomeCF)
    
    nome = input("Inserisci il tuo nome ")
    nomeCF = calcola_nome_cf(nome)
    #print (nomeCF)
    
    while True:
        try:
            sesso = input("Inserisci il sesso (m/f) ")
            if sesso not in ['f', 'female', 'femmina', 'm', 'male', 'maschio']:
                raise ValueError("Inserisci un sesso valido (f, female, femmina, m, male, maschio)")
            
            print("Data di nascita")
            giorno = int(input("Inserisci il giorno del mese in cui sei nato "))
            mese = int(input("Inserisci il mese in cui sei nato in formato numerico 1-12 "))
            anno = int(input("Inserisci l'anno di nascita "))
            if not (1 <= giorno <= 31 and 1 <= mese <= 12):
                raise ValueError("Data non valida")        
            dataCF = calcola_data_cf(sesso, giorno, mese, anno)
            break
            
        except ValueError as e:
            print("errore", e)
            print("inserisci i dati corretti \n" )
    while True:
        print("Luogo di nascita ")
        comune = input("Inserisci la citta' di nascita ")
        provincia = input("Provincia ")
        try:
            codice_catastale = get_codice_catastale(comune, provincia, codici)
            #print(codice_catastale)
            break
        except CodiceCatastaleNonTrovato as e:
            print("errore", e)
            print("inserisci i dati corretti di citta' e provincia \n" )
      

    cf15 = cognomeCF + nomeCF + dataCF + codice_catastale
    #print (cf15)        
    cf = cf15 + calcola_carattere_controllo(cf15)
    print("Il tuo codice fiscale: ", cf)
    risposta = input("Vuoi continuare? (s/n): ").strip().lower()
    if risposta != 's':
        print("Programma terminato.")
        break
