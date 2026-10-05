# Lekcja 5 — ORM: zapytania i relacje między tabelami

**Czas:** 45–90 min  
**Cel:** autor jako osobna tabela, kategorie, lista książek na stronie (nie tylko w adminie).

## Cele lekcji

Po lekcji uczeń:

- używa `ForeignKey` i `ManyToManyField`
- filtruje dane: `all()`, `filter()`, `get()`, `exclude()`
- wyświetla queryset w szablonie
- rozumie `related_name` i zapytanie odwrotne

## Teoria

| Relacja | W Django | Przykład |
|---------|----------|----------|
| 1:N | `ForeignKey` | wiele książek → jeden autor |
| N:N | `ManyToManyField` | książka ma wiele kategorii |
| 1:1 | `OneToOneField` | profil użytkownika |

**QuerySet** to „leniwe” zapytanie SQL. SQL leci do bazy dopiero przy użyciu wyniku (pętla, `list()`, `len()`).

```python
Ksiazka.objects.filter(dostepna=True, rok__gte=2020)
```

`__gte` = greater than or equal. Inne: `__icontains`, `__lt`, `__in`.

`get()` zwraca **jeden** obiekt albo wyjątek (`DoesNotExist` / `MultipleObjectsReturned`). Do listy używaj `filter()`.

## Ćwiczenie na lekcji

### 1. Nowe modele

Rozbuduj `katalog/models.py` (zostaw `Ksiazka`, zmień pole `autor`):

```python
from django.db import models


class Autor(models.Model):
    imie = models.CharField(max_length=80)
    nazwisko = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "Autorzy"
        ordering = ["nazwisko", "imie"]

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa


class Ksiazka(models.Model):
    tytul = models.CharField(max_length=200)
    autor = models.ForeignKey(
        Autor,
        on_delete=models.PROTECT,
        related_name="ksiazki",
    )
    kategorie = models.ManyToManyField(Kategoria, blank=True, related_name="ksiazki")
    rok = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    dostepna = models.BooleanField(default=True)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.tytul
```

`on_delete=models.PROTECT` — nie skasujesz autora, jeśli ma książki (bezpieczniej na lekcji niż `CASCADE`).

### 2. Migracje

Jeśli wcześniej `autor` było `CharField`, Django zapyta o wartości domyślne albo każe usunąć dane. W klasie:

- albo usuń `db.sqlite3` i zrób `migrate` od zera (i ponownie `createsuperuser` + książki),
- albo nauczyciel pomaga przy `makemigrations` (bardziej zaawansowane).

**Rekomendacja na zajęcia:** świeża baza, 5 książek wpisanych od nowa w adminie.

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Admin

```python
from django.contrib import admin
from .models import Autor, Kategoria, Ksiazka


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nazwisko", "imie")


@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nazwa",)


@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ("tytul", "autor", "rok", "dostepna")
    list_filter = ("dostepna", "kategorie")
    filter_horizontal = ("kategorie",)
```

Dodaj 3 autorów, 4 kategorie, 6 książek.

### 4. Widok listy i szczegółów

`katalog/views.py` — dopisz:

```python
from django.shortcuts import get_object_or_404, render
from .models import Ksiazka


def lista_ksiazek(request):
    ksiazki = Ksiazka.objects.select_related("autor").prefetch_related("kategorie")
    return render(request, "katalog/lista.html", {"ksiazki": ksiazki})


def szczegoly_ksiazki(request, pk):
    ksiazka = get_object_or_404(Ksiazka, pk=pk)
    return render(request, "katalog/szczegoly.html", {"ksiazka": ksiazka})
```

`get_object_or_404` — brak rekordu = strona 404, nie crash.

W `katalog/urls.py`:

```python
path("ksiazki/", views.lista_ksiazek, name="lista_ksiazek"),
path("ksiazki/<int:pk>/", views.szczegoly_ksiazki, name="szczegoly_ksiazki"),
```

### 5. Szablony

`lista.html` (extends `base.html`):

```django
{% extends "katalog/base.html" %}
{% block tytul %}Katalog{% endblock %}
{% block tresc %}
<h2>Książki</h2>
<ul>
    {% for k in ksiazki %}
        <li>
            <a href="{% url 'szczegoly_ksiazki' k.pk %}">{{ k.tytul }}</a>
            — {{ k.autor }}
            {% if not k.dostepna %}(wypożyczona){% endif %}
        </li>
    {% empty %}
        <li>Brak książek w katalogu.</li>
    {% endfor %}
</ul>
{% endblock %}
```

`szczegoly.html`: autor, rok, ISBN, kategorie (`{% for kat in ksiazka.kategorie.all %}`), opis.

Dodaj link „Katalog” w menu `base.html`.

## Shell Django (pokaz nauczyciela, 5 min)

```powershell
python manage.py shell
```

```python
from katalog.models import Autor, Ksiazka

Autor.objects.count()
Ksiazka.objects.filter(dostepna=True)
a = Autor.objects.first()
a.ksiazki.all()  # related_name
```

## Zadanie domowe

1. Na liście pokaż tylko książki `dostepna=True` **albo** dodaj parametr `?wszystkie=1` (dla chętnych).
2. W shellu wykonaj `filter(tytul__icontains="pan")` i zapisz wynik.

## Pytania kontrolne

1. Kiedy `ForeignKey`, a kiedy `ManyToManyField`?
2. Czym `filter` różni się od `get`?
3. Po co `get_object_or_404`?
4. Co robi `on_delete=PROTECT`?

## Dla nauczyciela

- `select_related` / `prefetch_related` — wspomnij jako „mniej zapytań SQL”, bez wykładu o N+1.
- Uczniowie często piszą `ksiazka.kategorie` zamiast `ksiazka.kategorie.all` w szablonie.
