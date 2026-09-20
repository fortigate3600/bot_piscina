import requests
import time

# --- CONFIGURAZIONE TEST A PROVA DI BOMBA ---
# Inseriamo i dati fissi senza usare variabili dinamiche o GitHub Secrets
ID_UTENTE = "70750"
data_target = "20260926"  # Il sabato che avevi intercettato originariamente
ORARIO_DESIDERATO = "10:00"
# --------------------------------------------

headers = {
    "Host": "appyfit.it",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "it.appifit.atlantidesportingclub",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; NX809J Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Origin": "https://localhost",
    "Referer": "https://localhost/",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

def prenota_piscina_test():
    print(f"🛠 TEST: Cerco i corsi per il {data_target} alle {ORARIO_DESIDERATO}...")
    timestamp_lista = int(time.time() * 1000)
    
    # Costruiamo l'URL esattamente identico a quello che l'app aveva generato
    url_lista = f"https://appyfit.it/Api/prenota/corso/?IDCS=86&idU={ID_UTENTE}&idcategoria=12&dataDiRicerca={data_target}&_={timestamp_lista}"
    
    response_lista = requests.get(url_lista, headers=headers, timeout=10)
    
    if response_lista.status_code != 200:
        print(f"❌ Errore HTTP {response_lista.status_code} nel recupero della lista.")
        return

    try:
        dati_corsi = response_lista.json()
        print("✅ LISTA RECUPERATA CON SUCCESSO! Il server non è crashato.")
    except Exception as e:
        print("❌ Il server ha risposto, ma non era un JSON valido.")
        return

    id_corso_da_prenotare = None

    for corso in dati_corsi.get("ListCorsi", []):
        if corso["DalOrarioCorso"] == ORARIO_DESIDERATO:
            prenotati = int(corso["strNumeroPrenotazioni"])
            massimi = int(corso["strNumeroPartecipanti"])
            
            print(f"✅ Trovato slot delle {ORARIO_DESIDERATO}! Posti: {prenotati}/{massimi}")
            
            if prenotati >= massimi:
                print("⚠️ Il corso è già pieno, test interrotto.")
                return
            
            id_corso_da_prenotare = corso["id_Corso"]
            break

    if id_corso_da_prenotare:
        print(f"🚀 Procedo con la prenotazione di test: {id_corso_da_prenotare}")
        timestamp_prenota = int(time.time() * 1000)
        url_prenota = f"https://appyfit.it/Api/prenota/corso/?IDCS=86&idU={ID_UTENTE}&idC={id_corso_da_prenotare}&idcategoria=12&I=1&dataDiRicerca={data_target}&nameCat=Nuoto%20libero&IDMicro=30&_={timestamp_prenota}"
        
        response_prenota = requests.get(url_prenota, headers=headers)
        
        if response_prenota.status_code == 200:
            print("🎉 Test riuscito! Vai sull'app per disdire questa prenotazione di prova.")
        else:
            print(f"❌ Errore {response_prenota.status_code} nella prenotazione.")
    else:
        print("❌ Nessun corso trovato a quell'ora.")

prenota_piscina_test()
