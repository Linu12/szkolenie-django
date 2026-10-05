from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Kategoria

# Create your views here.

def index(request):
    return render(request, 'blog/index.html', context={'title': 'Home'})
def about(request):
    return render(request, 'blog/about.html', context={'title': 'About'})
# def contact(request):
#     return HttpResponse("Contact page")
def contact(request):
    return render(request, 'blog/contact.html', context={'title': 'Contact'})
def lista_postow(request):
    posty = Post.objects.filter(opublikowany=True)
    return render(request, 'blog/lista_postow.html', {
        'posty': posty
        })