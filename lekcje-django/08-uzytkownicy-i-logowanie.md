# Lekcja 8 — Użytkownicy, sesje i uprawnienia

**Czas:** 45–90 min  
**Cel:** rejestracja, logowanie, wylogowanie; dodawanie książek tylko dla zalogowanych.

## Cele lekcji

Po lekcji uczeń:

- korzysta z wbudowanego modelu `User`
- używa widoków `LoginView` / `LogoutView`
- chroni widok dekoratorem `@login_required`
- pokazuje inną nawigację dla gościa i ucznia

## Teoria

HTTP jest **bezstanowy**. **Sesja** (ciasteczko + zapis po stronie serwera) pamięta, kto jest zalogowany.

Django ma `django.contrib.auth`: hasła są **haszowane** (nie trzymamy jawnego hasła w bazie).

| Narzędzie | Zastosowanie |
|-----------|----------------|
| `@login_required` | musi być zalogowany |
| `@staff_member_required` | personel / admin |
| `user.has_perm(...)` | konkretne uprawnienie |
| `user.is_superuser` | pełnia praw |

**Nie piszemy** własnego „czy hasło == hasło z pliku tekstowego”.

## Ćwiczenie na lekcji

### 1. Ustawienia przekierowań

W `config/settings.py` (na końcu):

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "lista_ksiazek"
LOGOUT_REDIRECT_URL = "strona_glowna"
```

### 2. URL-e logowania

W `config/urls.py` możesz dodać:

```python
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "konto/login/",
        auth_views.LoginView.as_view(template_name="katalog/login.html"),
        name="login",
    ),
    path(
        "konto/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("", include("katalog.urls")),
]
```

Wylogowanie w nowszym Django wymaga **POST** (nie link GET).

### 3. Szablon logowania

`katalog/templates/katalog/login.html`:

```django
{% extends "katalog/base.html" %}
{% block tytul %}Logowanie{% endblock %}
{% block tresc %}
<h2>Zaloguj się</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Wejdź</button>
</form>
{% endblock %}
```

### 4. Rejestracja

`katalog/forms.py`:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RejestracjaForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
```

`UserCreationForm` już ma hasło + powtórzenie hasła.

Widok:

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RejestracjaForm, KsiazkaForm


def rejestracja(request):
    if request.method == "POST":
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("lista_ksiazek")
    else:
        form = RejestracjaForm()
    return render(request, "katalog/rejestracja.html", {"form": form})
```

Szablon analogiczny do logowania (`form` + csrf). URL `konto/rejestracja/` w `katalog/urls.py` albo w `config/urls.py`.

### 5. Ochrona dodawania / edycji / usuwania

```python
@login_required
def nowa_ksiazka(request):
    ...
```

To samo na `edytuj_ksiazke` i `usun_ksiazke`.

Gość wchodzący na `/ksiazki/nowa/` wyląduje na logowaniu, potem wróci (parametr `next`).

### 6. Menu w `base.html`

```django
<nav>
    <a href="{% url 'strona_glowna' %}">Start</a>
    <a href="{% url 'lista_ksiazek' %}">Katalog</a>
    {% if user.is_authenticated %}
        <a href="{% url 'nowa_ksiazka' %}">Dodaj</a>
        <span>Cześć, {{ user.username }}</span>
        <form action="{% url 'logout' %}" method="post" style="display:inline">
            {% csrf_token %}
            <button type="submit">Wyloguj</button>
        </form>
    {% else %}
        <a href="{% url 'login' %}">Zaloguj</a>
        <a href="{% url 'rejestracja' %}">Rejestracja</a>
    {% endif %}
</nav>
```

`user` jest w szablonach dzięki context processorowi auth — nie musisz go przekazywać z każdego widoku.

### 7. Konta testowe

- superuser z lekcji 4 (admin)
- zwykły uczeń przez rejestrację

Zwykły user **nie** wchodzi do `/admin/` (chyba że `is_staff`).

## Zadanie na plus

Tylko `is_staff` może usuwać książki:

```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def usun_ksiazke(request, pk):
    ...
```

W szablonie szczegółów przycisk „Usuń” w `{% if user.is_staff %}`.

## Zadanie domowe

Opisz w 8–10 zdaniach: sesja, haszowanie hasła, po co `login_required`, dlaczego logout jest POST.

## Pytania kontrolne

1. Gdzie Django trzyma informację „jesteś zalogowany”?
2. Co zrobi `@login_required`, gdy gość wejdzie na chroniony URL?
3. Czym różni się superuser od zwykłego `User`?
4. Dlaczego nie logujemy się linkiem GET na wylogowanie?

## Dla nauczyciela

- Uczniowie często zostawiają `DEBUG` i słabe hasła — na lekcji OK, na internecie nie.
- Jeśli `LogoutView` zwraca 405 — brak POST.
- Nie łączcie konta admina z hasłem „admin/admin” przy pokazie na projektorze, jeśli sieć szkolna jest współdzielona; użyjcie jednorazowego hasła.
