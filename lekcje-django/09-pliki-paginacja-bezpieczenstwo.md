# Lekcja 9 — Media, paginacja, komunikaty i bezpieczeństwo

**Czas:** 45–90 min  
**Cel:** okładka książki, podział listy na strony, flash messages; świadome nawyki bezpieczeństwa.

## Cele lekcji

Po lekcji uczeń:

- dodaje `ImageField` i serwuje pliki w trybie deweloperskim
- używa `Paginator`
- pokazuje `messages.success` po zapisie
- wymienia podstawowe zagrożenia aplikacji web i mechanizmy Django

## Teoria — bezpieczeństwo (15 min, bez exploitów)

Mówimy **co chronić i jak Django pomaga**, bez instrukcji ataku.

| Temat | Dobra praktyka w Django |
|-------|-------------------------|
| CSRF | `{% csrf_token %}`, middleware |
| XSS | szablony escapują `{{ zmienna }}`; ostrożnie z `\|safe` |
| hasła | `auth`, nigdy plaintext |
| SQL injection | ORM zamiast sklejania SQL |
| sekrety | `SECRET_KEY` i hasła poza Git (`DEBUG=False` na produkcji) |
| uprawnienia | nie ufaj ukrytemu przyciskowi w HTML — sprawdzaj w widoku |

`SECRET_KEY` w `settings.py` podpisuje sesje. W projekcie szkolnym zostaje lokalnie; na serwerze bierze się z zmiennej środowiskowej.

## Ćwiczenie A — komunikaty

Na górze `base.html`, w `main`:

```django
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

W widoku po `form.save()`:

```python
from django.contrib import messages

messages.success(request, "Książka została zapisana.")
return redirect("lista_ksiazek")
```

Po usunięciu: `messages.info(...)`.

## Ćwiczenie B — paginacja

Lista może mieć 50 pozycji. W widoku:

```python
from django.core.paginator import Paginator
from .models import Ksiazka


def lista_ksiazek(request):
    qs = Ksiazka.objects.select_related("autor").order_by("tytul")
    paginator = Paginator(qs, 5)
    strona = request.GET.get("page")
    ksiazki = paginator.get_page(strona)
    return render(request, "katalog/lista.html", {"ksiazki": ksiazki})
```

W szablonie pod listą:

```django
{% if ksiazki.has_other_pages %}
    <p>
        {% if ksiazki.has_previous %}
            <a href="?page={{ ksiazki.previous_page_number }}">Poprzednia</a>
        {% endif %}
        Strona {{ ksiazki.number }} / {{ ksiazki.paginator.num_pages }}
        {% if ksiazki.has_next %}
            <a href="?page={{ ksiazki.next_page_number }}">Następna</a>
        {% endif %}
    </p>
{% endif %}
```

Dodaj w adminie więcej książek, żeby zobaczyć strony.

## Ćwiczenie C — okładka (media)

### 1. Pole i pakiet obrazków

```powershell
pip install Pillow
```

W modelu `Ksiazka`:

```python
okladka = models.ImageField("Okładka", upload_to="okladki/", blank=True, null=True)
```

```powershell
python manage.py makemigrations
python manage.py migrate
```

W `KsiazkaForm` dodaj `okladka` do `fields`.

Widoki z plikami **muszą** dostać `request.FILES`:

```python
form = KsiazkaForm(request.POST, request.FILES)
# edycja:
form = KsiazkaForm(request.POST, request.FILES, instance=ksiazka)
```

Formularz HTML:

```django
<form method="post" enctype="multipart/form-data">
```

Bez `enctype` plik **nie dojdzie**.

### 2. Ustawienia

W `config/settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

W `config/urls.py` (tylko przy `DEBUG`):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

W szczegółach książki:

```django
{% if ksiazka.okladka %}
    <img src="{{ ksiazka.okladka.url }}" alt="Okładka" width="160">
{% endif %}
```

Folder `media/` nie idzie do Gita (dodaj w `.gitignore`).

## Wyszukiwarka (krótko, jeśli starczy czasu)

Na liście:

```python
q = request.GET.get("q", "").strip()
if q:
    qs = qs.filter(tytul__icontains=q)
```

Formularz `method="get"` **bez** csrf (GET nie zmienia danych).

## Zadanie domowe

1. Paginacja + wyszukiwarka naraz: zachowaj `q` w linkach stron (`?q=...&page=2`).
2. Lista 5 zasad bezpieczeństwa „co wolno / czego nie wolno” w projekcie Django (bez opisu ataków).

## Pytania kontrolne

1. Po co `enctype="multipart/form-data"`?
2. Czym `MEDIA` różni się od `STATIC`?
3. Dlaczego `{{ tytul }}` jest bezpieczniejsze niż wklejanie HTML z `|safe`?
4. Gdzie sprawdzamy uprawnienia — w szablonie, w widoku, czy w obu? (oba: UI + serwer)

## Dla nauczyciela

- Limit rozmiaru uploadu można wspomnieć (`DATA_UPLOAD_MAX_MEMORY_SIZE`) bez konfiguracji na siłę.
- Nie instalujcie przypadkowych paczek z nieznanych źródeł.
- To dobra lekcja na kartkówkę teoretyczną pod INF.04 (warstwy, sesja, CSRF hasłowo).
