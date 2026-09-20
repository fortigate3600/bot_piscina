import requests
import time
import os
from datetime import datetime, timedelta

# --- CONFIGURAZIONE TEST LUNEDÌ ---
ID_UTENTE = os.environ.get("ID_UTENTE", "70750")
ORARIO_DESIDERATO = "10:00" # Slot delle 10:00 - 11:30

# Essendo oggi Domenica, calcoliamo la data per domani (Lunedì) aggiungendo 1 giorno
data_target = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
# ----------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; NX809J Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
    "X-Requested-With": "it.appifit.atlantidesportingclub",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

def prenota_piscina_test():
    print(f"🛠 TEST MODE: Cerco i corsi per domani {data_target} alle ore {ORARIO_DESIDERATO}...")
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
            
            print(f"✅ Trovato slot delle {ORARIO_DESIDERATO}! Posti occupati: {prenotati}/{massimi}")
            
            if prenotati >= massimi:
                print("⚠️ Il corso è già pieno, impossibile testare la prenotazione.")
                return
            
            id_corso_da_prenotare = corso["id_Corso"]
            break

    if id_corso_da_prenotare:
        print(f"🚀 Procedo con la prenotazione di test: {id_corso_da_prenotare}")
        timestamp_prenota = int(time.time() * 1000)
        url_prenota = f"https://appyfit.it/Api/prenota/corso/?IDCS=86&idU={ID_UTENTE}&idC={id_corso_da_prenotare}&idcategoria=12&I=1&dataDiRicerca={data_target}&nameCat=Nuoto%20libero&IDMicro=30&_={timestamp_prenota}"
        
        response_prenota = requests.get(url_prenota, headers=headers)
        
        if response_prenota.status_code == 200:
            print("🎉 Test riuscito! Vai a controllare sull'app se ti vedi prenotato.")
        else:
            print(f"❌ Errore HTTP {response_prenota.status_code} durante la prenotazione.")
    else:
        print("❌ Nessun corso trovato a quell'ora per domani.")

prenota_piscina_test()
