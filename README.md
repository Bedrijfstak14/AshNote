# AshNote

## 📝 AshNote – Your Personal Cigar Journal

<img src="static/ashnote-logo.png" alt="AshNote logo" width="200" height="auto">

AshNote is a minimalist yet powerful web application that helps you manage your cigar collection with ease. Whether you're a novice or a seasoned aficionado, you can effortlessly track which cigars you’ve smoked, where you bought them, what you thought of them, and even attach a photo and notes.

The app runs entirely in Docker and supports multiple users with administrator privileges for managing users. Everything runs locally — no external accounts or internet connection required.

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
ADMIN_USERNAME=admin          # The system administrator
```

3. **Start the app with Docker Compose**

```bash
docker-compose up --build -d
```

4. **Open the app in your browser**

Go to: [http://localhost:5005](http://localhost:5005)

---

## 🔐 User Management

* You can register a new account via the registration page.
* The administrator (as defined in `ADMIN_USERNAME`) has access to the **Admin page**, which includes:

  * Viewing all users
  * Deleting users
  * Resetting user passwords

---

## 📦 Data Storage

* Images: `data/uploads/`
* SQLite database: `data/cigars.db`
* Static files: `static/`

---

## ✨ Features

* Multi-user support
* Login & registration
* Personal cigar log
* Notes field per cigar
* Photo upload
* Search & sort functionality
* Account overview
* Per-user statistics
* Admin panel for user management

---

## 🧪 Development Tips

* Changes to `.env` require restarting the container:

```bash
docker-compose down
docker-compose up --build -d
```

* Database is automatically initialized on first run (SQLite).

---

# 🇳🇱 AshNote – Je persoonlijke sigarenlogboek

<img src="static/ashnote-logo.png" alt="AshNote logo" width="200" height="auto">

AshNote is een minimalistische maar krachtige webapplicatie waarmee je je sigarenverzameling eenvoudig kunt beheren. Of je nu een beginnende liefhebber bent of een doorgewinterde aficionado, met AshNote kun je moeiteloos bijhouden welke sigaren je hebt gerookt, waar je ze hebt gekocht, wat je ervan vond, en zelfs een foto en opmerkingen toevoegen.

De app draait volledig in Docker en ondersteunt meerdere gebruikers, met beheerdersrechten voor gebruikersbeheer. Alles is lokaal: geen externe accounts of internetverbinding nodig.

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
ADMIN_USERNAME=admin          # De beheerder van het systeem
```

3. **Start de app met Docker Compose**

```bash
docker-compose up --build -d
```

4. **Open de app in je browser**

Ga naar: [http://localhost:5005](http://localhost:5005)

---

## 🔐 Gebruikersbeheer

* Je maakt een account aan via de registratiesectie.
* De beheerder (zoals ingesteld via `ADMIN_USERNAME`) krijgt toegang tot een **Admin-pagina** met:

  * Lijst van alle gebruikers
  * Mogelijkheid om gebruikers te verwijderen
  * Wachtwoorden van gebruikers te resetten

---

## 📦 Gegevensopslag

* Afbeeldingen: `data/uploads/`
* SQLite database: `data/cigars.db`
* Statische bestanden: `static/`

---

## ✨ Functionaliteiten

* Meerdere gebruikers
* Login & registratie
* Persoonlijk sigarenoverzicht
* Opmerkingenveld per sigaar
* Foto-upload
* Zoeken & sorteren
* Account-overzicht
* Statistieken per gebruiker
* Admin-pagina voor gebruikersbeheer

---

## 🧪 Ontwikkelingstips

* Wijzigingen in `.env` vereisen herstart van de container:

```bash
docker-compose down
docker-compose up --build -d
```

* Database wordt automatisch aangemaakt bij het opstarten (SQLite).