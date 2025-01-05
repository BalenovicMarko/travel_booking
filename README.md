Zadatak je napraviti aplikaciju pomoću djanga. Moja tema je aplikacija za rezervaciju putovanja i smještaja. Ovo su neke funkcionalnosti koje ova aplikacija za sada ima: 
1. Autentifikacija
Omogućeno je prijavljivanje korisnika u sustav koristeći e-mail adresu ili korisničko ime i lozinku. Koristi se Django-ov ugrađeni User model za autentifikaciju.

2. Autorizacija
Aplikacija omogućuje različite razine pristupa:
Administrator: Potpuni pristup sustavu, uključujući uređivanje i brisanje podataka te pristup svim dijelovima aplikacije.
Korisnik: Ograničen pristup. Može pregledavati podatke, ali ne i mijenjati ih.

3. Upravljanje korisnicima
Administrator ima mogućnost:
Kreiranja novih korisničkih računa.
Uređivanja postojećih korisnika.
Brisanja korisničkih računa.

4. Generički pogledi (ListView i DetailView)
ListView:
Prikazuje popis svih objekata s ključnim informacijama.
Omogućeno je filtriranje i pretraživanje po atributima kao što su kategorija, datum kreiranja ili korisnik.
DetailView:
Prikazuje sve detalje o pojedinom objektu, uključujući relacije (ako postoje).

5. CRUD Funkcionalnosti
Create (Dodavanje):
Omogućeno dodavanje novih objekata putem web forme uz validaciju podataka.
Nakon uspješnog unosa, korisnik se preusmjerava na ListView ili DetailView novog objekta.
Read (Čitanje):
Pregled svih objekata uz filtriranje i pretraživanje kroz ListView.
Detalji pojedinog objekta dostupni su putem DetailView.
Update (Ažuriranje):
Omogućeno ažuriranje postojećih objekata putem forme s validacijom.
Nakon izmjena, korisnik se preusmjerava na DetailView ažuriranog objekta.
Delete (Brisanje):
Implementirana funkcionalnost za brisanje objekata uz potvrdu korisnika.
Nakon brisanja, korisnik se preusmjerava na ListView.

6. Testni podaci
Kreirani su testni podaci kako bi:
Pokrili sve ključne funkcionalnosti aplikacije.
Omogućili smislen prikaz u ListView i DetailView pogledima.

7. Pretraživanje
Dodana funkcionalnost pretraživanja unutar ListView prikaza kako bi se olakšalo pronalaženje objekata po ključnim atributima.



Na ovom projektu radi samo: Marko Balenović
