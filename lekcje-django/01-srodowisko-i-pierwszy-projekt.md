# Lekcja 1 — Środowisko i pierwszy projekt Django

**Czas:** 45–90 min  
**Cel:** zainstalować Django w venv i zobaczyć działającą stronę w przeglądarce.

## Cele lekcji

Po lekcji uczeń:

- wyjaśnia, czym jest framework Django i wzorzec MVT
- tworzy środowisko wirtualne na Windows
- tworzy projekt `startproject` i uruchamia serwer deweloperski
- otwiera stronę powitalną Django

## Teoria (10–15 min)

**Django** to framework Pythona do aplikacji webowych. Dostarcza routing, szablony HTML, ORM (baza danych), panel administracyjny i ochronę przed typowymi atakami (m.in. CSRF).

**MVT** (Model–View–Template):

| Warstwa | Rola | Przykład |
|---------|------|----------|
| Model | dane w bazie | książka, uczeń |
| View | logika (Python) | „pobierz listę książek” |
| Template | wygląd (HTML) | strona z tabelą |

**Projekt vs aplikacja:** projekt to cały serwis (ustawienia, URL główne). Aplikacja (`app`) to jeden moduł, np. `katalog`.

**Środowisko wirtualne (`venv`)** izoluje paczki projektu od reszty komputera. W technikum **zawsze** pracujemy w venv.

## Przygotowanie komputera

Sprawdź Pythona w PowerShell:

```powershell
python --version
```

Powinno być **3.10+**. Jeśli polecenie nie działa, spróbuj `py --version`.

Utwórz folder kursu, np. `C:\kurs\biblioteka`.

## Ćwiczenie na lekcji (krok po kroku)

### 1. Folder i venv

```powershell
mkdir biblioteka-szkolna
cd biblioteka-szkolna
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jeśli PowerShell zablokuje skrypt:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Prompt powinien zaczynać się od `(.venv)`.

### 2. Instalacja Django

```powershell
python -m pip install --upgrade pip
pip install django
python -m django --version
```

### 3. Projekt

Nazwa projektu: `config` (ustawienia). Aplikację dodamy na lekcji 2.

```powershell
django-admin startproject config .
```

Kropka na końcu oznacza: „twórz pliki tutaj, nie w podfolderze”.

Struktura:

```
biblioteka-szkolna/
  .venv/
  manage.py
  config/
    settings.py
    urls.py
    ...
```

`manage.py` — narzędzie: serwer, migracje, tworzenie aplikacji.

### 4. Migracje startowe i serwer

```powershell
python manage.py migrate
python manage.py runserver
```

Otwórz w przeglądarce: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Powinna pojawić się rakieta / strona sukcesu Django.

**Zatrzymanie serwera:** `Ctrl + C` w terminalu.

### 5. Mini zmiana (opcjonalnie, jeśli starczy czasu)

W `config/urls.py` nic jeszcze nie ruszamy — to lekcja 2.  
Na dziś wystarczy: **venv + install + startproject + runserver**.

## Typowe błędy

| Objaw | Przyczyna | Co zrobić |
|-------|-----------|-----------|
| `Activate.ps1` zabroniony | ExecutionPolicy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `django-admin` nieznane | venv wyłączony | aktywuj `.venv` ponownie |
| port zajęty | inny `runserver` | `python manage.py runserver 8001` |
| strona nie wstaje | zły folder | `manage.py` musi być w bieżącym katalogu |

## Zadanie domowe

1. Zrób zrzut ekranu działającej strony Django (adres `127.0.0.1:8000`).
2. W 5–7 zdaniach opisz różnicę między **projektem** a **aplikacją** oraz po co jest **venv**.
3. Zapisz w notatce komendy: tworzenie venv, aktywacja, `startproject`, `runserver`.

## Pytania kontrolne

1. Co oznacza MVT?
2. Do czego służy `manage.py`?
3. Dlaczego nie instalujemy Django „na cały system” bez venv?
4. Jaki adres ma serwer deweloperski Django?

## Dla nauczyciela

- Sprawdź, czy u wszystkich działa venv (najczęstszy problem na Windows).
- Nie przechodź do URL-i, dopóki cała klasa nie zobaczy strony powitalnej.
- Uczniowie nie commitują folderu `.venv`.
