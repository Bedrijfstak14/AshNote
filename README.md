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

---

# 🇺🇸 English Version

## 📝 AshNote – Your Personal Cigar Journal

<img src="static/ashnote-logo.png" alt="AshNote logo" width="200" height="auto">

AshNote is a minimalist yet powerful web application that helps you manage your cigar collection with ease. Whether you're a novice or a seasoned aficionado, you can effortlessly track which cigars you've smoked, where you bought them, what you thought of them, and even attach a photo and notes.

The app runs entirely in Docker and supports multiple users with administrator privileges for managing users. Everything works locally, but there's also external API integration for searching cigar data.

The interface is built with Bootstrap 5 and optimized for both desktop and mobile use.

---

## ⚙️ Installation (Docker)

1. **Clone this repository**

```bash
git clone https://github.com/Bedrijfstak14/AshNote.git
cd AshNote
```

2. **Create a `.env` file**

```env
SECRET_KEY=somethingStrongHere
ADMIN_USERNAME=admin                    # The system administrator
RAPIDAPI_KEY=your_api_key_here         # For external cigar data (optional)
RAPIDAPI_HOST=cigars.p.rapidapi.com    # API host for cigar data
```

3. **Start the app with Docker Compose**

```bash
docker-compose up --build -d
```

4. **Open the app in your browser**

Go to: [http://localhost:5006](http://localhost:5006)

---

## 🔐 User Management

* Create an account via the registration page
* The administrator (as defined in `ADMIN_USERNAME`) gets access to an **Admin page** with:
  * Overview of all users
  * Delete users (except themselves)
  * Reset user passwords

---

## 📦 Data Storage

* Images: `data/uploads/`
* SQLite database: `data/cigars.db`
* Static files: `static/`

---

## ✨ Features

### Cigar Management
* **Add cigars**: Add new cigars with photo, rating (1-10), country of origin, purchase location, price and notes
* **Edit cigars**: Modify existing cigars, including replacing photos
* **Delete cigars**: Remove cigars from your collection
* **Photo upload**: Upload images of your cigars
* **External API integration**: Search for cigar data via RapidAPI for automatic data filling

### Search and Sort
* **Search function**: Search by name, purchase location or country of origin
* **Sort options**: Sort by name, price, purchase location or country of origin
* **Responsive table**: Desktop and mobile display optimized

### User Functions
* **Multi-user support**: Multiple users can each manage their own cigar collection
* **Account overview**: See statistics like number of cigars, total value and most common purchase location
* **Change password**: Users can change their own password
* **Personal collection**: Each user only sees their own cigars

### Admin Functions
* **User management**: View all users
* **Delete users**: Remove users (and all their data)
* **Password reset**: Reset passwords of other users
* **Full control**: Admin has access to all management functions

---

## 🌐 API Integration

The application uses an external API for retrieving cigar data:
* **RapidAPI Cigars API**: For searching external cigar data
* **Automatic filling**: Fill form fields automatically based on API results
* **Optional**: The app also works without API access

---

## 📊 Statistics and Overviews

### Account Statistics
* Total number of cigars in collection
* Total value of the collection
* Most common purchase location
* Personal ratings

### Data Structure
Each cigar contains:
* Name (required)
* Rating 1-10 (required)
* Country of origin (optional)
* Purchase location (optional)
* Price in euros (optional)
* Notes (optional)
* Photo (optional)

---

## 🧪 Development Tips

* **Changes to `.env`** require container restart:

```bash
docker-compose down
docker-compose up --build -d
```

* **Database**: SQLite database is automatically created on first startup
* **File structure**: Uploads are stored in `data/uploads/`
* **Port mapping**: The app runs on port 8000 internally, mapped to 5006 externally
* **Volumes**: `./data:/app/data` ensures persistent storage

---

## 🔧 Technical Details

### Backend
* **Flask**: Python web framework
* **SQLAlchemy**: Database ORM
* **SQLite**: Local database
* **Werkzeug**: Security utilities
* **Requests**: For external API calls

### Frontend
* **Bootstrap 5**: Responsive UI framework
* **Jinja2**: Template engine
* **JavaScript**: For dynamic functionality (API search)

### Security
* **Password hashing**: Werkzeug password hashing
* **Session management**: Flask sessions
* **File upload security**: Secure filename handling
* **User isolation**: Users can only see/edit their own data

---

## 📋 Requirements

See `requirements.txt`:
* Flask==2.3.3
* Flask-SQLAlchemy==3.1.1
* python-dotenv
* requests

---

## 🐳 Docker Configuration

* **Base image**: python:3.11-slim
* **Working directory**: /app
* **Exposed port**: 8000
* **Volume mapping**: ./data:/app/data
* **Environment**: Via .env file
