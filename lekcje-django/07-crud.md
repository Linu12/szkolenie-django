# Lekcja 7 — CRUD: pełny cykl życia rekordu

**Czas:** 45–90 min  
**Cel:** lista, szczegóły, dodawanie, edycja i usuwanie książki.

## Cele lekcji

Po lekcji uczeń:

- implementuje Create, Read, Update, Delete
- przekazuje instancję do `ModelForm` (`instance=...`)
- stosuje potwierdzenie usunięcia (osobna strona POST)
- (opcjonalnie) poznaje widoki klasowe jako skrót

## Teoria

| Litera | HTTP | U nas |
|--------|------|--------|
| Create | POST | `/ksiazki/nowa/` |
| Read | GET | `/ksiazki/`, `/ksiazki/3/` |
| Update | POST | `/ksiazki/3/edycja/` |
| Delete | POST | `/ksiazki/3/usun/` |

Usuwanie **linkiem GET** (`<a href="...usun">`) jest błędem: robot / podgląd może skasować dane. Zawsze formularz POST + csrf.

## Ćwiczenie na lekcji

Masz już Create i Read. Dopisujesz Update i Delete.

### 1. Edycja

```python
from django.shortcuts import get_object_or_404, redirect, render
from .forms import KsiazkaForm
from .models import Ksiazka


def edytuj_ksiazke(request, pk):
    ksiazka = get_object_or_404(Ksiazka, pk=pk)
    if request.method == "POST":
        form = KsiazkaForm(request.POST, instance=ksiazka)
        if form.is_valid():
            form.save()
            return redirect("szczegoly_ksiazki", pk=ksiazka.pk)
    else:
        form = KsiazkaForm(instance=ksiazka)
    return render(
        request,
        "katalog/formularz.html",
        {"form": form, "naglowek": f"Edycja: {ksiazka.tytul}"},
    )
```

Ten sam szablon `formularz.html` — inny nagłówek.

URL:

```python
path("ksiazki/<int:pk>/edycja/", views.edytuj_ksiazke, name="edytuj_ksiazke"),
```

Na stronie szczegółów:

```django
<a href="{% url 'edytuj_ksiazke' ksiazka.pk %}">Edytuj</a>
```

### 2. Usuwanie z potwierdzeniem

```python
def usun_ksiazke(request, pk):
    ksiazka = get_object_or_404(Ksiazka, pk=pk)
    if request.method == "POST":
        ksiazka.delete()
        return redirect("lista_ksiazek")
    return render(request, "katalog/potwierdz_usuniecie.html", {"ksiazka": ksiazka})
```

`potwierdz_usuniecie.html`:

```django
{% extends "katalog/base.html" %}
{% block tresc %}
<h2>Usunąć „{{ ksiazka.tytul }}”?</h2>
<p>Tej operacji nie cofniesz (na lekcji nie ma kosza).</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Tak, usuń</button>
</form>
<a href="{% url 'szczegoly_ksiazki' ksiazka.pk %}">Anuluj</a>
{% endblock %}
```

URL:

```python
path("ksiazki/<int:pk>/usun/", views.usun_ksiazke, name="usun_ksiazke"),
```

### 3. Checklist ucznia

Na tablicy / kartkówce praktycznej:

- [ ] lista pokazuje książki
- [ ] szczegóły działają dla `pk`
- [ ] nowa książka pojawia się na liście
- [ ] edycja zmienia tytuł
- [ ] usunięcie wymaga POST i znika z listy
- [ ] zły `pk` → 404

## Opcja dla szybszych: widoki klasowe

To **nie zastępuje** zrozumienia funkcji. Pokaz 10 min:

```python
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Ksiazka


class KsiazkaLista(ListView):
    model = Ksiazka
    template_name = "katalog/lista.html"
    context_object_name = "ksiazki"
```

Reszta analogicznie (`CreateView`, `success_url`). Klasa 4 powinna umieć **obie** wersje na poziomie „wiem, że istnieją”.

## Zadanie domowe

Dodaj model `Wypozyczenie` (`ksiazka` FK, `imie_ucznia`, `data` `auto_now_add=True`) + lista wypożyczeń **albo** na stronie książki przycisk „Oznacz jako wypożyczoną” (ustawia `dostepna=False` POST-em).

## Pytania kontrolne

1. Po co `instance=ksiazka` w formularzu?
2. Dlaczego usuwanie nie może być zwykłym linkiem GET?
3. Co zwraca `delete()` na modelu?
4. Jak uniknąć podwójnego zapisu przy F5 po POST?

## Dla nauczyciela

- Kartkówka: „narysuj URL-e CRUD”.
- Słabsi: tylko edycja. Szybsi: klasowe widoki albo wypożyczenia.
- Uczniowie mylą `pk` w URL z `id` w szablonie — w Django `pk` jest aliasem klucza głównego.
