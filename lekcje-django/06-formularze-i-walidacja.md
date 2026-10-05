# Lekcja 6 — Formularze Django i walidacja

**Czas:** 45–90 min  
**Cel:** dodać książkę ze strony (nie tylko z `/admin/`), z ochroną CSRF.

## Cele lekcji

Po lekcji uczeń:

- rozróżnia GET (pokaz formularza) i POST (zapis)
- używa `ModelForm`
- wstawia `{% csrf_token %}`
- pokazuje błędy walidacji przy polach

## Teoria

Bez frameworka dane z `<form>` trzeba czytać z `request.POST` i samemu sprawdzać. **Django Form / ModelForm** mapuje pola, waliduje, zwraca błędy.

**CSRF** (Cross-Site Request Forgery) — obca strona mogłaby wysłać POST w imieniu zalogowanego ucznia. Token w formularzu + middleware Django to blokuje.

**Złota zasada:** zmiana danych tylko metodą POST (lub DELETE/PUT w API). GET tylko odczyt.

Przepływ:

```text
GET /ksiazki/nowa/  → pusty formularz
POST               → is_valid()? tak → save() → przekierowanie
                   → nie → ten sam szablon z błędami
```

Po udanym POST: **redirect** (wzór PRG — Post/Redirect/Get), żeby odświeżenie strony nie dodawało rekordu drugi raz.

## Ćwiczenie na lekcji

### 1. Formularz

Nowy plik `katalog/forms.py`:

```python
from django import forms
from .models import Ksiazka


class KsiazkaForm(forms.ModelForm):
    class Meta:
        model = Ksiazka
        fields = ["tytul", "autor", "kategorie", "rok", "isbn", "dostepna", "opis"]
        widgets = {
            "opis": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_rok(self):
        rok = self.cleaned_data["rok"]
        if rok < 1450 or rok > 2100:
            raise forms.ValidationError("Podaj realistyczny rok wydania.")
        return rok
```

`clean_<pole>` — własna walidacja. Do zapisu używaj `cleaned_data`, nie surowego POST.

### 2. Widok

```python
from django.shortcuts import redirect, render
from .forms import KsiazkaForm


def nowa_ksiazka(request):
    if request.method == "POST":
        form = KsiazkaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_ksiazek")
    else:
        form = KsiazkaForm()
    return render(request, "katalog/formularz.html", {"form": form, "naglowek": "Nowa książka"})
```

URL:

```python
path("ksiazki/nowa/", views.nowa_ksiazka, name="nowa_ksiazka"),
```

**Kolejność path:** `ksiazki/nowa/` **przed** `ksiazki/<int:pk>/`, inaczej słowo `nowa` może być źle interpretowane (tu `pk` jest `int`, więc konflikt mniejszy — i tak ucz dobrego porządku: konkretne ścieżki wyżej).

### 3. Szablon

`katalog/templates/katalog/formularz.html`:

```django
{% extends "katalog/base.html" %}
{% block tytul %}{{ naglowek }}{% endblock %}
{% block tresc %}
<h2>{{ naglowek }}</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Zapisz</button>
</form>
<p><a href="{% url 'lista_ksiazek' %}">Anuluj</a></p>
{% endblock %}
```

Na start `as_p` wystarczy. Później można rozpisać pola ręcznie (`{{ form.tytul }}`, `{{ form.tytul.errors }}`).

### 4. Link w menu / na liście

```django
<a href="{% url 'nowa_ksiazka' %}">Dodaj książkę</a>
```

### 5. Testy przy tablicy

- pusty tytuł → błąd
- rok `300` → Wasz `clean_rok`
- ten sam ISBN dwa razy → błąd unikalności
- poprawne dane → widać pozycję na liście

Wyłącz na chwilę `{% csrf_token %}` (pokaz) — POST powinien dostać **403 Forbidden**. Potem token wraca.

## Zadanie na plus

Owiń pola w CSS (klasy w `widgets` albo `form.as_p` + `form p { margin-bottom: 0.5rem; }`).

## Zadanie domowe

Dodaj w modelu pole `jezyk` (np. `CharField` z `choices`: polski, angielski, inny), migracja, pole w formularzu.

## Pytania kontrolne

1. Po co `{% csrf_token %}`?
2. Czym `is_valid()` różni się od samego `request.POST`?
3. Dlaczego po zapisie robimy `redirect`, a nie `render` listy?
4. Kiedy użyć `ModelForm`, a kiedy zwykłego `forms.Form`?

## Dla nauczyciela

- Nie każ uczniom pisać ręcznego SQL INSERT.
- Mów wprost: **nigdy** nie wyłączamy CSRF „żeby działało”.
- `filter_horizontal` jest w adminie; w `ModelForm` M2M to lista wielokrotnego wyboru — OK na lekcję.
