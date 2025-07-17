# 🍽️ Chatbot Prenotazioni Ristorante - Rasa 3.x

Un chatbot intelligente per gestire le prenotazioni di un ristorante, sviluppato con **Rasa 3.x** e **Forms** per la raccolta strutturata delle informazioni cliente.

## 📋 Indice

- [Caratteristiche](#-caratteristiche)
- [Prerequisiti](#-prerequisiti)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Funzionalità](#-funzionalità)
- [Gestione Database](#-gestione-database)
- [Personalizzazione](#-personalizzazione)
- [Troubleshooting](#-troubleshooting)

## 🌟 Caratteristiche

- **Form Intelligenti**: Raccolta automatica di nome, email, telefono, data, ora e numero ospiti
- **Validazione Avanzata**: Controllo automatico di tutti i campi con messaggi di errore personalizzati
- **Database Persistente**: Salvataggio automatico delle prenotazioni in SQLite
- **Gestione Flessibile**: Supporta diversi formati di input (date, orari, numeri)
- **Controllo Disponibilità**: Verifica automatica delle disponibilità
- **Esportazione Dati**: Export delle prenotazioni in CSV
- **Interfaccia di Gestione**: Script per visualizzare e gestire le prenotazioni

## 🔧 Prerequisiti

- **Python 3.8+**
- **pip** (package manager)
- **Git** (opzionale, per clonare il repository)

## 📦 Installazione

### 1. Clona il repository
```bash
git clone <URL_REPOSITORY>
cd rasa-restaurant-bot
```

### 2. Crea ambiente virtuale
```bash
python -m venv chatbot_env
source chatbot_env/bin/activate  # Linux/Mac
# chatbot_env\Scripts\activate   # Windows
```

### 3. Installa le dipendenze
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Crea file `actions/__init__.py`
```bash
touch actions/__init__.py  # Linux/Mac
echo. > actions/__init__.py  # Windows
```

## 🚀 Utilizzo

### Avvio del Sistema

1. **Addestra il modello**:
   ```bash
   rasa train
   ```

2. **Avvia l'action server** (Terminal 1):
   ```bash
   rasa run actions
   ```

3. **Avvia il chatbot** (Terminal 2):
   ```bash
   rasa shell
   ```

### Esempio di Conversazione

```
🤖 Ciao! Benvenuto al Ristorante Bella Vista! Come posso aiutarti oggi?
👤 vorrei prenotare un tavolo

🤖 Perfetto! Iniziamo con la prenotazione. Come ti chiami?
👤 Mario Rossi

🤖 Grazie Mario Rossi! Puoi fornirmi la tua email?
👤 francesco@email.com

🤖 Ottimo! Ora ho bisogno del tuo numero di telefono...
👤 3401234567

🤖 Per quale data vorresti prenotare? (formato: gg/mm/aaaa)
👤 25/12/2025

🤖 A che ora preferiresti cenare? (formato: hh:mm)
👤 20:00

🤖 Per quante persone sarà la prenotazione?
👤 4

🤖 Perfetto Francesco Paolo Ragusa! La tua prenotazione è confermata:
    📋 ID Prenotazione: #1
    📅 Data: 25/12/2025
    🕐 Ora: 20:00
    👥 Persone: 4
    📧 Email: francesco@email.com
    📞 Telefono: 3401234567
```

## 📁 Struttura del Progetto

```
rasa-restaurant-bot/
├── README.md                          # Documentazione principale
├── .gitignore                         # File di esclusione Git
├── requirements.txt                   # Dipendenze Python
├── domain.yml                         # Configurazione domain Rasa
├── config.yml                         # Pipeline NLU e policies
├── endpoints.yml                      # Configurazione endpoints
├── database.py                        # Gestione database SQLite
├── view_reservations.py               # Script gestione prenotazioni
├── data/                              # Training data
│   ├── nlu.yml                        # Esempi NLU
│   ├── stories.yml                    # Training stories
│   └── rules.yml                      # Regole conversazione
├── actions/                           # Custom actions
│   ├── __init__.py                    # File inizializzazione
│   └── actions.py                     # Validazione e logica business
├── models/                            # Modelli addestrati (auto-generata)
├── reservations.db                    # Database SQLite (auto-generato)
└── chatbot_env/                       # Ambiente virtuale
```

## 🎯 Funzionalità

### Form di Prenotazione

Il chatbot raccoglie automaticamente:

| Campo | Validazione | Formati Supportati |
|-------|-------------|-------------------|
| **Nome** | Min 2 caratteri, solo lettere | "Mario Rossi", "Anna" |
| **Email** | Formato email valido | "user@domain.com" |
| **Telefono** | 10-15 cifre | "3401234567", "+39 340 123 4567" |
| **Data** | Formato gg/mm/aaaa, futuro | "25/12/2025", "oggi", "domani" |
| **Orario** | 18:00-23:00 | "20:00", "otto", "otto e mezza" |
| **Ospiti** | 1-12 persone | "4", "quattro", "due persone" |

### Validazione Intelligente

- **Email**: Controllo regex per formato valido
- **Telefono**: Pulizia automatica e controllo lunghezza
- **Data**: Verifica che non sia nel passato, max 3 mesi
- **Orario**: Conversione testo-numero, orari di apertura
- **Ospiti**: Supporto numerico e testuale

### Gestione Errori

- Messaggi di errore specifici per ogni campo
- Richiesta automatica di correzione
- Mantenimento del contesto durante la validazione

## 🗄️ Gestione Database

### Visualizzazione Prenotazioni

```bash
# Tutte le prenotazioni
python view_reservations.py view

# Prenotazioni di oggi
python view_reservations.py today

# Menu interattivo
python view_reservations.py

# Esporta in CSV
python view_reservations.py export
```

### Menu Interattivo

```
🍽️  GESTIONE PRENOTAZIONI RISTORANTE
==================================================
1. Visualizza tutte le prenotazioni
2. Prenotazioni di oggi
3. Prenotazioni per data specifica
4. Esporta in CSV
5. Cancella prenotazione
6. Statistiche
0. Esci
```

### Operazioni Database

```python
from database import ReservationDatabase

# Crea istanza database
db = ReservationDatabase()

# Visualizza tutte le prenotazioni
db.print_all_reservations()

# Prenotazioni per data
reservations = db.get_reservations_by_date("25/12/2025")

# Esporta in CSV
from database import export_to_csv
export_to_csv("prenotazioni_dicembre.csv")
```

## 🔧 Personalizzazione

### Modifica Orari di Apertura

Nel file `actions/actions.py`, funzione `validate_reservation_time()`:

```python
# Cambia gli orari di apertura
opening_time = datetime.strptime("17:00", "%H:%M").time()  # Apre alle 17:00
closing_time = datetime.strptime("24:00", "%H:%M").time()  # Chiude a mezzanotte
```

### Aggiungi Nuovi Campi

1. **Aggiungi slot nel `domain.yml`**:
   ```yaml
   slots:
     special_requests:
       type: text
       mappings:
       - type: from_text
         conditions:
         - active_loop: restaurant_form
           requested_slot: special_requests
   ```

2. **Aggiungi al form**:
   ```yaml
   forms:
     restaurant_form:
       required_slots:
         - customer_name
         - customer_email
         - customer_phone
         - reservation_date
         - reservation_time
         - number_of_guests
         - special_requests  # Nuovo campo
   ```

3. **Aggiungi validazione in `actions.py`**:
   ```python
   def validate_special_requests(self, slot_value, dispatcher, tracker, domain):
       if slot_value and len(slot_value) > 500:
           dispatcher.utter_message(text="La richiesta è troppo lunga. Max 500 caratteri.")
           return {"special_requests": None}
       return {"special_requests": slot_value}
   ```

### Modifica Messaggi

Nel file `domain.yml`, sezione `responses`:

```yaml
responses:
  utter_greet:
  - text: "Benvenuto al Mio Ristorante! Come posso aiutarti?"
  
  utter_ask_customer_name:
  - text: "Come ti chiami?"
  
  # Aggiungi nuovi messaggi...
```

## 🐛 Troubleshooting

### Problemi Comuni

**1. Errore: "Cannot find module 'database'"**
```bash
# Verifica che database.py sia nella root
ls -la database.py

# Testa l'import
python -c "from database import ReservationDatabase; print('OK')"
```

**2. Form non si attiva**
```bash
# Verifica che RulePolicy sia abilitata in config.yml
grep -A 5 "RulePolicy" config.yml

# Riaddestra il modello
rasa train
```

**3. Action server non trova le azioni**
```bash
# Verifica che actions/__init__.py esista
ls -la actions/__init__.py

# Riavvia l'action server
rasa run actions
```

**4. Database non salva**
```bash
# Verifica permessi di scrittura
touch test_write.db && rm test_write.db

# Controlla errori nell'action server
# (guarda il terminal dove gira "rasa run actions")
```

**5. Validazione non funziona**
```bash
# Verifica che validate_restaurant_form sia in domain.yml
grep "validate_restaurant_form" domain.yml

# Riaddestra dopo modifiche
rasa train
```

### Debug Avanzato

```bash
# Avvia in modalità debug
rasa shell --debug

# Testa singole actions
rasa run actions --debug

# Verifica training data
rasa data validate
```

## 📊 Performance e Monitoring

### Statistiche Utilizzo

```python
# Statistiche prenotazioni
python view_reservations.py
# Seleziona opzione 6 per statistiche
```

### Backup Database

```bash
# Backup manuale
cp reservations.db backup_$(date +%Y%m%d).db

# Backup automatico (Linux/Mac)
crontab -e
# Aggiungi: 0 2 * * * cp /path/to/reservations.db /path/to/backup_$(date +\%Y\%m\%d).db
```

## 🤝 Contribuire

1. **Fork** il repository
2. **Crea** un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

### Linee Guida per Contribuire

- Scrivi test per le nuove funzionalità
- Aggiorna la documentazione
- Segui lo stile del codice esistente
- Descrivi chiaramente le modifiche nella PR

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Ringraziamenti

- **Rasa Team** per il framework conversazionale
- **Community Rasa** per esempi e supporto
- **Contributori** del progetto

## 📞 Supporto

Per supporto, apri una **Issue** su GitHub o contatta:

- **Email**: support@restaurant-bot.com
- **Discord**: [Server della Community](https://discord.gg/restaurant-bot)
- **Forum**: [Discussioni GitHub](https://github.com/user/repo/discussions)

---

**Fatto con ❤️ e Rasa 3.x**

*Ultimo aggiornamento: Luglio 2025*
