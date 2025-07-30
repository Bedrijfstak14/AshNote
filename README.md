# AshNote



## 📝 AshNote – Je persoonlijke sigarenlogboek

<img src="static/ashnote-logo.png" alt="AshNote logo" width="200" height="auto">

AshNote is een minimalistische maar krachtige webapplicatie waarmee je je sigarenverzameling eenvoudig kunt beheren. Of je nu een beginnende liefhebber bent of een doorgewinterde aficionado, met AshNote kun je moeiteloos bijhouden welke sigaren je hebt gerookt, waar je ze hebt gekocht, wat je ervan vond, en zelfs een foto en opmerkingen toevoegen.

De app draait volledig in Docker en ondersteunt meerdere gebruikers, met beheerdersrechten voor gebruikersbeheer. Alles werkt lokaal, maar er is ook een externe API-integratie voor het zoeken naar sigarengegevens.

De interface is gebouwd met Bootstrap 5 en is geoptimaliseerd voor desktop én mobiel gebruik.

---

## ⚙️ Installatie (Docker)

1. **Clone deze repository**

```bash
git clone https://github.com/Bedrijfstak14/AshNote.git
cd AshNote
```

2. **Maak een `.env` bestand aan**

```env
SECRET_KEY=ietsSterksHier
ADMIN_USERNAME=admin                    # De beheerder van het systeem
RAPIDAPI_KEY=jouw_api_key_hier         # Voor externe sigarendata (optioneel)
RAPIDAPI_HOST=cigars.p.rapidapi.com    # API host voor sigarendata
```

3. **Start de app met Docker Compose**

```bash
docker-compose up --build -d
```

4. **Open de app in je browser**

Ga naar: [http://localhost:5006](http://localhost:5006)

---

## 🔐 Gebruikersbeheer

* Je maakt een account aan via de registratiepagina
* De beheerder (zoals ingesteld via `ADMIN_USERNAME`) krijgt toegang tot een **Admin-pagina** met:
  * Overzicht van alle gebruikers
  * Gebruikers verwijderen (behalve zichzelf)
  * Wachtwoorden van gebruikers resetten

---

## 📦 Gegevensopslag

* Afbeeldingen: `data/uploads/`
* SQLite database: `data/cigars.db`
* Statische bestanden: `static/`

---

## ✨ Functionaliteiten

### Sigarenbeheer
* **Sigaren toevoegen**: Voeg nieuwe sigaren toe met foto, beoordeling (1-10), land van herkomst, aankooplocatie, prijs en opmerkingen
* **Sigaren bewerken**: Pas bestaande sigaren aan, inclusief het vervangen van foto's
* **Sigaren verwijderen**: Verwijder sigaren uit je collectie
* **Foto-upload**: Upload afbeeldingen van je sigaren
* **Externe API-integratie**: Zoek naar sigarengegevens via RapidAPI voor automatische gegevensinvulling

### Zoeken en sorteren
* **Zoekfunctie**: Zoek op naam, aankooplocatie of land van herkomst
* **Sorteeropties**: Sorteer op naam, prijs, aankooplocatie of land van herkomst
* **Responsieve tabel**: Desktop en mobiele weergave geoptimaliseerd

### Gebruikersfuncties
* **Multi-user support**: Meerdere gebruikers kunnen elk hun eigen sigarencollectie beheren
* **Account-overzicht**: Zie statistieken zoals aantal sigaren, totale waarde en meest voorkomende aankooplocatie
* **Wachtwoord wijzigen**: Gebruikers kunnen hun eigen wachtwoord wijzigen
* **Persoonlijke collectie**: Elke gebruiker ziet alleen zijn eigen sigaren

### Admin-functies
* **Gebruikersbeheer**: Bekijk alle gebruikers
* **Gebruikers verwijderen**: Verwijder gebruikers (en al hun gegevens)
* **Wachtwoord reset**: Reset wachtwoorden van andere gebruikers
* **Volledige controle**: Admin heeft toegang tot alle beheerfuncties

---

## 🌐 API-integratie

De applicatie maakt gebruik van een externe API voor het ophalen van sigarengegevens:
* **RapidAPI Cigars API**: Voor het zoeken naar externe sigarendata
* **Automatische invulling**: Vul formuliervelden automatisch in op basis van API-resultaten
* **Optioneel**: De app werkt ook zonder API-toegang

---

## 📊 Statistieken en overzichten

### Account-statistieken
* Totaal aantal sigaren in collectie
* Totale waarde van de collectie
* Meest voorkomende aankooplocatie
* Persoonlijke beoordelingen

### Gegevensstructuur
Elke sigaar bevat:
* Naam (verplicht)
* Beoordeling 1-10 (verplicht)
* Land van herkomst (optioneel)
* Aankooplocatie (optioneel)
* Prijs in euro's (optioneel)
* Opmerkingen (optioneel)
* Foto (optioneel)

---

## 🧪 Ontwikkelingstips

* **Wijzigingen in `.env`** vereisen herstart van de container:

```bash
docker-compose down
docker-compose up --build -d
```

* **Database**: SQLite database wordt automatisch aangemaakt bij eerste opstarten
* **Bestandsstructuur**: Uploads worden opgeslagen in `data/uploads/`
* **Port mapping**: De app draait op poort 8000 intern, gemapped naar 5006 extern
* **Volumes**: `./data:/app/data` zorgt voor persistente opslag

---

## 🔧 Technische details

### Backend
* **Flask**: Python web framework
* **SQLAlchemy**: Database ORM
* **SQLite**: Lokale database
* **Werkzeug**: Security utilities
* **Requests**: Voor externe API-calls

### Frontend
* **Bootstrap 5**: Responsive UI framework
* **Jinja2**: Template engine
* **JavaScript**: Voor dynamische functionaliteit (API-zoeken)

### Security
* **Wachtwoord hashing**: Werkzeug password hashing
* **Session management**: Flask sessions
* **File upload security**: Secure filename handling
* **User isolation**: Gebruikers kunnen alleen eigen data zien/bewerken

---

## 📋 Requirements

Zie `requirements.txt`:
* Flask==2.3.3
* Flask-SQLAlchemy==3.1.1
* python-dotenv
* requests

---

## 🐳 Docker configuratie

* **Base image**: python:3.11-slim
* **Working directory**: /app
* **Exposed port**: 8000
* **Volume mapping**: ./data:/app/data
* **Environment**: Via .env bestand
