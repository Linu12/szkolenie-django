# Lekcja 3 — Szablony HTML i pliki statyczne (CSS)

**Czas:** 45–90 min  
**Cel:** wspólny layout strony (jak na lekcjach HTML) + menu działające przez `{% url %}`.

## Cele lekcji

Po lekcji uczeń:

- renderuje szablon przez `render()`
- stosuje dziedziczenie szablonów (`extends`, `block`)
- wstawia zmienne i pętle DTL (Django Template Language)
- podłącza CSS przez `{% static %}`

## Teoria

Widok **nie** powinien sklejać dużego HTML w Pythonie. HTML leży w `katalog/templates/katalog/`.

**Dziedziczenie:** `base.html` ma nagłówek, menu, stopkę. Podstrony wypełniają tylko `{% block tresc %}`.

To ten sam pomysł co Wasz układ `header` / `nav` / `main` / `footer`.

Przykład DTL:

```django
<h1>{{ tytul }}</h1>
{% for pozycja in menu %}
  <li>{{ pozycja }}</li>
{% endfor %}
```

## Ćwiczenie na lekcji

### 1. Foldery

```
katalog/
  templates/
    katalog/
      base.html
      index.html
      o_nas.html
      kontakt.html
  static/
    katalog/
      style.css
```

### 2. `base.html`

```django
{% load static %}
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block tytul %}Biblioteka szkolna{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'katalog/style.css' %}">
</head>
<body>
    <header>
        <h1>Biblioteka szkolna</h1>
    </header>
    <nav>
        <a href="{% url 'strona_glowna' %}">Start</a>
        <a href="{% url 'o_nas' %}">O bibliotece</a>
        <a href="{% url 'kontakt' %}">Kontakt</a>
    </nav>
    <main>
        {% block tresc %}{% endblock %}
    </main>
    <footer>
        <p>Technikum — Django, lekcja 3</p>
    </footer>
</body>
</html>
```

### 3. Podstrony

`index.html`:

```django
{% extends "katalog/base.html" %}

{% block tytul %}Start — Biblioteka{% endblock %}

{% block tresc %}
<section>
    <h2>{{ powitanie }}</h2>
    <p>Liczba sal lekcyjnych w szkole (przykład z widoku): {{ sale }}</p>
    <ul>
        {% for dzial in dzialy %}
            <li>{{ dzial }}</li>
        {% empty %}
            <li>Brak działów.</li>
        {% endfor %}
    </ul>
</section>
{% endblock %}
```

`o_nas.html` i `kontakt.html` — analogicznie, z własnym tekstem w `{% block tresc %}`.

### 4. CSS (nawiązanie do Waszego `style.css`)

`katalog/static/katalog/style.css`:

```css
header {
    background-color: rgb(248, 100, 100);
    border-radius: 10px;
    padding: 1rem;
}
nav {
    background-color: rgb(75, 169, 245);
    border-radius: 10px;
    padding: 1rem;
    margin: 1% 0;
}
nav a {
    margin-right: 1rem;
    color: #111;
}
main {
    background-color: rgb(110, 244, 110);
    border-radius: 10px;
    min-height: 300px;
    padding: 1rem;
}
footer {
    background-color: rgb(245, 49, 190);
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1%;
}
```

### 5. Widoki z `render`

W `katalog/views.py`:

```python
from django.shortcuts import render


def strona_glowna(request):
    kontekst = {
        "powitanie": "Witaj w katalogu biblioteki",
        "sale": 24,
        "dzialy": ["Lektury", "Informatyka", "Języki obce"],
    }
    return render(request, "katalog/index.html", kontekst)


def o_nas(request):
    return render(request, "katalog/o_nas.html")


def kontakt(request):
    return render(request, "katalog/kontakt.html")
```

Uruchom serwer i odśwież strony. Menu ma działać bez ręcznego wpisywania adresów.

## Zadanie na plus

W `base.html` dodaj `aside` (panel boczny) jak w `index.html` z zajęć HTML: godziny otwarcia. Użyj `display: flex` na kontenerze `main + aside`.

## Zadanie domowe

1. Dodaj stronę `regulamin.html` + widok + URL `regulamin/`.
2. W szablonie startowym użyj `{% if sale > 20 %}` i pokaż komunikat „Duża szkoła”.

## Pytania kontrolne

1. Po co `{% load static %}`?
2. Czym różni się `{{ zmienna }}` od `{% znacznik %}`?
3. Co zrobi Django, gdy szablon nie istnieje?
4. Dlaczego w menu używamy `{% url 'kontakt' %}`, a nie `/kontakt/` na sztywno?

## Dla nauczyciela

- `DEBUG=True` serwuje static sam. Przy `DEBUG=False` trzeba `collectstatic` — to na później.
- Częsty błąd: szablon w złym folderze (`templates/index.html` zamiast `templates/katalog/index.html`).
