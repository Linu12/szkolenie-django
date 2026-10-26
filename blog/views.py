
from django.http import HttpResponse
from .models import Post, Tag, Kategoria
from .forms import KontaktForm
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'blog/index.html', context={'title': 'Home'})
def about(request):
    return render(request, 'blog/about.html', context={'title': 'About'})
# def contact(request):
#     return HttpResponse("Contact page")
# def contact(request):
#     return render(request, 'blog/contact.html', context={'title': 'Contact'})
def lista_postow(request):
    posty = Post.objects.filter(opublikowany=True)
    return render(request, 'blog/lista_postow.html', {
        'posty': posty
        })


def contact(request):
    if request.method == 'POST':
        form = KontaktForm(request.POST)

        if form.is_valid():
            imie = form.cleaned_data['imie']
            email = form.cleaned_data['email']
            wiadomosc = form.cleaned_data['wiadomosc']

            print("=== NOWA WIADOMOŚĆ ===")
            print("Imię:", imie)
            print("Email:", email)
            print("Wiadomość:", wiadomosc)
            print("======================")

            return render(
                request,
                'blog/contact_success.html',
                {'title': 'Contact'}
            )

        else:
            print("Błędy formularza:", form.errors)

    else:
        form = KontaktForm()

    return render(request, 'blog/contact.html', {
        'title': 'Contact',
        'form': form,
    })