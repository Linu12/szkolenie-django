# Lekcja 10 — Projekt zaliczeniowy: Biblioteka szkolna 1.0

**Czas:** 90 min (lub 2 bloki) + dokończenie w domu  
**Cel:** spiąć lekcje 1–9 w jedną aplikację i obronić ją przy komputerze.

## Cele lekcji

Po lekcji uczeń:

- ma działający projekt spełniający wymagania minimalne
- potrafi uruchomić go z venv i pokazać przepływ MVT
- nazywa pliki: `models.py`, `views.py`, `urls.py`, szablon, `settings.py`

## Wymagania na ocenę

### Na 3 (musi działać)

- venv + Django, `runserver`
- layout: `base.html` + CSS
- model książki (min. tytuł, autor, dostępność)
- lista + szczegóły
- panel `/admin/` z superuserem
- `csrf_token` w formularzach POST

### Na 4

Wszystko z „na 3” oraz:

- `ForeignKey` lub `ManyToMany`
- dodawanie i edycja przez `ModelForm`
- usuwanie POST z potwierdzeniem
- `@login_required` na zmianę danych
- rejestracja albo tylko konta z `createsuperuser` + 1 zwykły user (uzgodnij z nauczycielem)

### Na 5

Wszystko z „na 4” oraz **co najmniej 3** z listy:

- okładka (`ImageField`)
- paginacja
- wyszukiwarka tytułu
- komunikaty `messages`
- wypożyczenie (osobny model albo flaga + historia)
- ograniczenie usuwania do `is_staff`
- własna walidacja (`clean_...`)
- czytelny README: jak uruchomić (3–6 linijek)

## Przebieg zajęć

1. **10 min** — checklista na tablicy, uczniowie odhaczają braki.
2. **60 min** — praca własna, nauczyciel krąży (migracje, 404, csrf, static).
3. **20 min** — obrona: 3 pytania przy stanowisku (poniżej).

Nie zaczynajcie nowego motywu (REST, Docker, chmura) kosztem dokończenia CRUD.

## Pytania na obronę (losuj 3)

1. Śledź żądanie `/ksiazki/2/` od URL do szablonu.
2. Po co migracje? Co zrobiłeś po dodaniu pola?
3. Różnica GET i POST na przykładzie usuwania.
4. Co robi `login_required`?
5. Gdzie leży CSS i jak trafia do HTML?
6. Czym model różni się od formularza?
7. Po co `SECRET_KEY` i `DEBUG`? (hasłowo, bez procedur ataku)
8. Jak Django chroni przed wklejeniem skryptu w tytule książki? (escape w szablonie)

## Kryteria oceny projektu (propozycja 40 pkt)

| Kryterium | Punkty |
|-----------|--------|
| Uruchomienie i struktura katalogów | 6 |
| Modele i migracje | 6 |
| Szablony i nawigacja | 6 |
| CRUD | 8 |
| Auth / uprawnienia | 6 |
| Extra (media, paginacja, …) | 5 |
| Obrona ustna | 3 |

## Co **nie** jest wymagane

- deploy na internet
- PostgreSQL
- REST API / DRF
- testy automatyczne (chętni mogą dodać 1 test widoku)
- Bootstrap / Tailwind (czysty CSS wystarczy)

## Uruchomienie — ściąga dla ucznia

```powershell
cd sciezka\do\biblioteka-szkolna
.\.venv\Scripts\Activate.ps1
pip install django pillow
python manage.py migrate
python manage.py runserver
```

## Zadanie po kursie (nieobowiązkowe)

Krótka notatka: jedna rzecz, którą dodałbyś w wersji 2.0 (np. terminy zwrotu, maile, role bibliotekarz/uczeń) i **które** elementy Django byś do tego użył.

## Dla nauczyciela — schemat oceniania braków

- projekt nie wstaje: max 2, chyba że uczeń naprawi na obronie
- działa tylko admin, brak własnych szablonów: max 3-
- skopiowany kod bez rozumienia URL/widok: obniz obronę, nie całość jeśli aplikacja spełnia wymagania
- wyłączony CSRF / `DEBUG` jako „rozwiązanie błędu”: rozmowa i poprawka na miejscu

## Mapowanie na podstawę / egzamin

Uczeń po 10 lekcjach powinien umieć w praktyce: warstwy aplikacji web, CRUD, sesja, formularz, relacyjna baza przez ORM — to rdzeń zadań praktycznych z Pythona + web w technikum.
