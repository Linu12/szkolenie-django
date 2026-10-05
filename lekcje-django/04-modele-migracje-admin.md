# Lekcja 4 — Modele, baza SQLite i panel admina

**Czas:** 45–90 min  
**Cel:** zapisać książki w bazie i edytować je w `/admin/`.

## Cele lekcji

Po lekcji uczeń:

- definiuje model Django (`class` dziedzicząca po `models.Model`)
- tworzy i wgrywa migracje
- rejestruje model w adminie
- tworzy superużytkownika

## Teoria

**Model** = tabela w bazie. Django ORM tłumaczy Pythona na SQL.

Domyślna baza: **SQLite** (`db.sqlite3`) — plik, wystarczy na lekcje. W firmie często PostgreSQL.

**Migracja** to przepis na zmianę struktury tabeli (jak Git, ale dla schematu bazy):

```text
zmiana w models.py  →  makemigrations  →  migrate
```

Bez `migrate` nowa kolumna **nie istnieje** w bazie.

## Ćwiczenie na lekcji

### 1. Model `Ksiazka`

W `katalog/models.py`:

```python
from django.db import models


class Ksiazka(models.Model):
    tytul = models.CharField("Tytuł", max_length=200)
    autor = models.CharField("Autor", max_length=120)
    rok = models.PositiveIntegerField("Rok wydania")
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    dostepna = models.BooleanField("Dostępna", default=True)
    opis = models.TextField("Opis", blank=True)

    class Meta:
        verbose_name = "Książka"
        verbose_name_plural = "Książki"
        ordering = ["tytul"]

    def __str__(self):
        return f"{self.tytul} ({self.autor})"
```

### 2. Migracje

```powershell
python manage.py makemigrations
python manage.py migrate
```

Sprawdź, że powstał plik w `katalog/migrations/0001_....py`.

### 3. Admin

W `katalog/admin.py`:

```python
from django.contrib import admin
from .models import Ksiazka


@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ("tytul", "autor", "rok", "dostepna")
    list_filter = ("dostepna", "rok")
    search_fields = ("tytul", "autor", "isbn")
```

### 4. Superuser

```powershell
python manage.py createsuperuser
```

Podaj: login, e-mail (może być fikcyjny szkolny), hasło (w terminalu **nie widać** znaków — to normalne).

### 5. Test

```powershell
python manage.py runserver
```

Wejdź na [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/), zaloguj się i dodaj **co najmniej 5 książek** (w tym 1 niedostępną).

## Język panelu (opcjonalnie)

W `config/settings.py`:

```python
LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_TZ = True
```

Restart serwera — menu admina po polsku.

## Zadanie na plus

Dodaj pole `liczba_stron = models.PositiveIntegerField(null=True, blank=True)`, potem:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Pokaż nauczycielowi nową kolumnę w adminie.

## Zadanie domowe

1. Dopisz do modelu pole `wydawnictwo` (`CharField`).
2. Wykonaj migracje.
3. Wklej do zeszytu / pliku tekstowego **trzy** komendy: `makemigrations`, `migrate`, `createsuperuser` i po co każda jest.

**Nie wysyłaj** pliku `db.sqlite3` z prawdziwym hasłem na pendrive kolegi bez potrzeby — baza zawiera konto admina.

## Pytania kontrolne

1. Czym jest ORM?
2. Co się stanie, gdy zmienisz model i **nie** zrobisz migracji?
3. Po co metoda `__str__`?
4. Czym `CharField` różni się od `TextField`?

## Dla nauczyciela

- Hasła uczniów: minimum 8 znaków; Django odrzuci zbyt proste.
- `unique=True` na ISBN — duplikat przy dodawaniu to dobra okazja, żeby pokazać błąd walidacji.
- Plik `db.sqlite3` można skasować i zrobić `migrate` od nowa, jeśli ktoś zepsuje bazę (straci dane).
