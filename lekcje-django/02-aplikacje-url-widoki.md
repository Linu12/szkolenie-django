# Lekcja 2 — Aplikacje, adresy URL i widoki

**Czas:** 45–90 min  
**Cel:** dodać aplikację `katalog` i trzy podstrony: start, o bibliotece, kontakt.

## Cele lekcji

Po lekcji uczeń:

- tworzy aplikację `startapp`
- rejestruje ją w `INSTALLED_APPS`
- pisze funkcje widoków (`HttpResponse`)
- łączy ścieżki w `urls.py` (projekt + aplikacja)

## Teoria

**Żądanie HTTP:** przeglądarka pyta serwer o adres, np. `/kontakt/`. Django:

1. szuka dopasowania w `urlpatterns`
2. wywołuje **widok** (funkcję Pythona)
3. widok zwraca **odpowiedź** (`HttpResponse` albo wyrenderowany szablon)

**Aplikacja** trzyma własną logikę. Dobrą praktyką jest plik `katalog/urls.py` i dołączenie go w `config/urls.py` przez `include()`.

## Ćwiczenie na lekcji

Pracujesz w folderze z lekcji 1, venv **aktywny**.

### 1. Aplikacja

```powershell
python manage.py startapp katalog
```

Powstanie folder `katalog/` (`views.py`, `models.py`, `admin.py`, …).

W `config/settings.py` dodaj aplikację:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "katalog",
]
```

### 2. Widoki

W `katalog/views.py`:

```python
from django.http import HttpResponse


def strona_glowna(request):
    return HttpResponse("<h1>Biblioteka szkolna</h1><p>Witaj w katalogu.</p>")


def o_nas(request):
    return HttpResponse("<h1>O bibliotece</h1><p>Wypożyczamy lektury i podręczniki.</p>")


def kontakt(request):
    return HttpResponse("<h1>Kontakt</h1><p>biblioteka@szkola.edu.pl</p>")
```

`request` to obiekt żądania (metoda GET/POST, użytkownik, dane formularza).

### 3. URL-e aplikacji

Nowy plik `katalog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.strona_glowna, name="strona_glowna"),
    path("o-nas/", views.o_nas, name="o_nas"),
    path("kontakt/", views.kontakt, name="kontakt"),
]
```

`name=` przyda się w szablonach (`{% url %}`) na lekcji 3.

### 4. URL-e projektu

W `config/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("katalog.urls")),
]
```

### 5. Test

```powershell
python manage.py runserver
```

Sprawdź:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- [http://127.0.0.1:8000/o-nas/](http://127.0.0.1:8000/o-nas/)
- [http://127.0.0.1:8000/kontakt/](http://127.0.0.1:8000/kontakt/)

## Zadanie na plus

Dodaj czwartą stronę `/godziny/` z godzinami otwarcia biblioteki (widok + `path`).

## Zadanie domowe

Narysuj (lub opisz listą) drogę żądania: przeglądarka → `config/urls.py` → `katalog/urls.py` → widok → HTML.

Dopisz w notatce, po co jest `include()` i `name=` w `path()`.

## Pytania kontrolne

1. Czym różni się `startproject` od `startapp`?
2. Co zwróci widok, jeśli zapomnisz `return`?
3. Co się stanie przy adresie, którego nie ma w `urlpatterns`? (kod 404)
4. Dlaczego ścieżki aplikacji trzymamy osobno, a nie wszystko w `config/urls.py`?

## Dla nauczyciela

- Pilnuj końcowego slasha: `kontakt/` vs `kontakt` — Django może przekierować, ale uczniowie się gubią.
- Na tym etapie **bez** szablonów plikowych — świadomie, żeby oddzielić routing od HTML.
