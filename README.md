# Travel Booking - Django aplikacija

## 📌 Zadatak
Zadatak je napraviti aplikaciju pomoću Djanga.  
Tema je aplikacija za **rezervaciju putovanja i smještaja**.
Autor ovoga projekta: Marko Balenović
---

## 🚀 Funkcionalnosti aplikacije

### 🔑 1. Autentifikacija
- Registracija novih korisnika.
- Prijava i odjava pomoću korisničkog imena i lozinke.
- Koristi se Django-ov ugrađeni **User model**.

### 👤 2. Autorizacija
- **Administrator:**
  - Potpuni pristup sustavu.
  - Može dodavati, uređivati i brisati sve podatke.
  - Upravljanje korisnicima i ponudama.
- **Korisnik:**
  - Može rezervirati smještaj i putovanja.
  - Ima uvid samo u vlastite rezervacije.
  - Može ažurirati i brisati vlastite rezervacije.

### 👥 3. Upravljanje korisnicima
- Administrator može:
  - Kreirati nove račune.
  - Uređivati postojeće korisnike.
  - Brisati korisnike.

### 📑 4. Generički pogledi (CBV)
- **ListView** – prikaz popisa objekata (ponude, smještaji, rezervacije).
- **DetailView** – detaljan prikaz jednog objekta.

### 🛠 5. CRUD funkcionalnosti
- **Create** – unos novih podataka putem forme.
- **Read** – pregled svih unosa i detaljan prikaz.
- **Update** – uređivanje postojećih podataka.
- **Delete** – brisanje uz potvrdu korisnika.

### 📊 6. Testni podaci
- Generirani testni podaci za demonstraciju funkcionalnosti.

### 🔍 7. Pretraživanje
- Mogućnost pretraživanja rezervacija po:
  - Nazivu smještaja,
  - Destinaciji,
  - Ponudi putovanja.

### ✅ 8. Testovi
- Implementirani testovi za:
  - URL-ove (ispravna navigacija),
  - View-ove (CRUD),
  - Forme (validacija),
  - Autentifikaciju i autorizaciju.

---

## 🛠 Tehnologije
- **Backend:** Python 3, Django
- **Frontend:** HTML, TailwindCSS, HTMX
- **Baza podataka:** SQLite (default, lako zamjenjiva)
- **Testiranje:** Django TestCase (unittest)

---

## 📦 Instalacija i pokretanje

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/BalenovicMarko/travel_booking.git
cd travel_booking-main #(Ako automatski nije otvoren u tom direktoriju)

# 2. Instaliraj potrebne pakete globalno (ili u svom sistemskom Pythonu)
pip install -r requirements.txt

# 3. Pokreni migracije
python manage.py migrate

# 4. Kreiraj superusera (admin korisnika) 
python manage.py createsuperuser

# 5. Učitaj inicijalne podatke
python manage.py loaddata initial_data.json #(Obavezno napraviti korisnika prije ove naredbe jer inače neće raditi)

# 6. Pokreni server
python manage.py runserver

# 7. Pristupi aplikaciji
# Aplikacija: http://127.0.0.1:8000
# Admin panel: http://127.0.0.1:8000/admin

