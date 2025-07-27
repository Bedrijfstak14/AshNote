# AshNote
## 📝 AshNote – Je persoonlijke sigarenlogboek

<img src="static/ashnote-logo.png" alt="AshNote logo" width="200" height="auto">

AshNote is een minimalistische maar krachtige webapplicatie waarmee je je sigarenverzameling eenvoudig kunt beheren. Of je nu een beginnende liefhebber bent of een doorgewinterde aficionado, met AshNote kun je moeiteloos bijhouden welke sigaren je hebt gerookt, waar je ze hebt gekocht, wat je ervan vond en zelfs een foto toevoegen.

De app draait volledig in Docker en maakt gebruik van een eenvoudige login op basis van gebruikersnaam en wachtwoord, ingesteld via een .env bestand. Je kunt direct beginnen met het toevoegen van sigaren via een gebruiksvriendelijk formulier, en alle gegevens worden veilig opgeslagen in een lokale SQLite-database. Afbeeldingen worden opgeslagen in een uploadmap op je schijf en zijn direct zichtbaar in het overzicht.

De interface is gebouwd met Bootstrap 5 en is geschikt voor zowel desktop als mobiel gebruik. Alles is lokaal en zonder afhankelijkheid van externe accounts of diensten.

---

### ⚙️ Installatie (Docker)

1. **Clone deze repository**

```bash
git clone https://github.com/Bedrijfstak14/AshNote.git
cd AshNote
```

2. **Maak een `.env` bestand aan**

Maak in de hoofdmap een `.env` bestand aan met de volgende inhoud:

```env
SECRET_KEY=ietsSterksHier
LOGIN_USER=user
LOGIN_PASS=supergeheim
```

> Let op: deze gegevens worden gebruikt voor de loginpagina.

3. **Start de app met Docker Compose**

```bash
docker-compose up --build -d
```

4. **Open de app in je browser**

Ga naar: [http://localhost:5005](http://localhost:5005)

---

* Afbeeldingen worden opgeslagen in `data/uploads/`
* De SQLite-database staat in `data/cigars.db`
* Statische bestanden zoals het logo staan in `static/`

---

### 🔐 Inloggen

Na het starten van de app moet je inloggen via de browser. Gebruik de gebruikersnaam en het wachtwoord uit het `.env` bestand:

```
Gebruikersnaam: admin
Wachtwoord: supergeheim
```

---

