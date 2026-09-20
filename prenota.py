import requests
import time
import os
from datetime import datetime, timedelta

# Configurazione
ID_UTENTE = os.environ.get("ID_UTENTE", "70750") # Prende l'ID dai Secret di GitHub (o usa 70750 di base)
ORARIO_DESIDERATO = "19:00"

# Calcola la data di 7 giorni nel futuro
data_target = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; NX809J Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
    "X-Requested-With": "it.appifit.atlantidesportingclub",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

def prenota_piscina():
    print(f"🔎 Cerco i corsi del {data_target} alle ore {ORARIO_DESIDERATO}...")
    timestamp_lista = int(time.time() * 1000)
    url_lista = f"https://appyfit.it/Api/prenota/corso/?IDCS=86&idU={ID_UTENTE}&idcategoria=12&dataDiRicerca={data_target}&_={timestamp_lista}"
    
    response_lista = requests.get(url_lista, headers=headers)
    
    if response_lista.status_code != 200:
        print("❌ Errore nel recupero della lista corsi.")
        return

    dati_corsi = response_lista.json()
    id_corso_da_prenotare = None

    for corso in dati_corsi.get("ListCorsi", []):
        if corso["DalOrarioCorso"] == ORARIO_DESIDERATO:
            prenotati = int(corso["strNumeroPrenotazioni"])
            massimi = int(corso["strNumeroPartecipanti"])
            
            print(f"✅ Trovato slot! Posti occupati: {prenotati}/{massimi}")
            
            if prenotati >= massimi:
                print("⚠️ Il corso è già pieno!")
                return
            
            id_corso_da_prenotare = corso["id_Corso"]
            break

    if id_corso_da_prenotare:
        print(f"🚀 Procedo con la prenotazione: {id_corso_da_prenotare}")
        timestamp_prenota = int(time.time() * 1000)
        url_prenota = f"https://appyfit.it/Api/prenota/corso/?IDCS=86&idU={ID_UTENTE}&idC={id_corso_da_prenotare}&idcategoria=12&I=1&dataDiRicerca={data_target}&nameCat=Nuoto%20libero&IDMicro=30&_={timestamp_prenota}"
        
        response_prenota = requests.get(url_prenota, headers=headers)
        
        if response_prenota.status_code == 200:
            print("🎉 Prenotazione effettuata con successo!")
        else:
            print(f"❌ Errore HTTP {response_prenota.status_code} durante la prenotazione.")
    else:
        print("❌ Nessun corso trovato a quell'ora.")

prenota_piscina()
