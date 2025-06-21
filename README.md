# ♠️ Poker Game Scraper & Discord Notifier

Un bot scraper scritto in **Python** che monitora in tempo reale una piattaforma di poker online, rileva quando iniziano nuove partite e invia automaticamente notifiche in un **canale Discord privato**.

---

## 🚀 Funzionalità principali

- 🔍 Scraping automatico delle pagine della piattaforma poker
- ♻️ Polling asincrono efficiente con `aiohttp`
- 📢 Integrazione con Discord via `discord.py`
- 🧠 Gestione dinamica dei driver con `webdriver-manager`
- 🔐 Utilizzo sicuro di variabili d’ambiente tramite `python-dotenv`

---

## 📦 Requisiti

- Python 3.8 o superiore
- Un token di **Discord Bot**
- Il file `.env` configurato (vedi sotto)
- Google Chrome installato (o un altro browser supportato da Selenium)

---

## 📁 Installazione

1. **Clona il repository**
   ```bash
   git clone https://github.com/tuo-username/poker-scraper-discord-bot.git
   cd poker-scraper-discord-bot
   ```

2. **Crea un ambiente virtuale (opzionale ma consigliato)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   .\venv\Scripts\activate       # Windows
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura il file `.env`**

   Crea un file `.env` nella root del progetto e aggiungi:

   ```env
   DISCORD_TOKEN=il_tuo_token_bot_discord
   CHANNEL_ID=123456789012345678
   SCRAPER_URL=https://link-piattaforma-poker.com
   ```

5. **Avvia il bot**
   ```bash
   python main.py
   ```

---

## 🧰 Librerie utilizzate

| Libreria            | Descrizione                                 |
|---------------------|---------------------------------------------|
| `aiohttp`           | Richieste HTTP asincrone per scraping       |
| `discord.py`        | Bot Discord avanzato                        |
| `selenium`          | Automazione browser per scraping dinamico   |
| `python-dotenv`     | Caricamento sicuro di variabili d’ambiente  |
| `webdriver-manager` | Gestione automatica del driver del browser  |

---

## 💬 Funzionamento

1. **Avvio del bot:** connessione al canale Discord privato specificato.
2. **Polling/scraping periodico:** il bot controlla a intervalli regolari l’attività di gioco.
3. **Match rilevati:** se vengono trovate nuove partite, i dati vengono formattati e inviati in Discord.
4. **Evitare duplicati:** mantiene uno stato interno per evitare spam con notifiche ripetute.

---

## 🛡️ Sicurezza

- Nessuna informazione sensibile è hardcoded.
- Tutte le credenziali vengono caricate da `.env`.

---

## 📌 Esempio di output su Discord

```
♠️ Nuova partita trovata!

Tavolo: High Stakes NLHE  
Giocatori: 6  
Buy-in: $200  
Stato: In corso  
```

---

## 📅 Roadmap / Possibili estensioni

- [ ] Aggiunta del supporto per più piattaforme
- [ ] Logging avanzato
- [ ] Pannello web di configurazione
- [ ] Deploy su server/VPS

---

## 🧑‍💻 Autore

Creato da [Pietro Piraino](https://github.com/PietroPiraino)  

---

## 📄 Licenza

Distribuito sotto licenza **MIT**.  
Libero uso e modifica per progetti personali o didattici.

---
