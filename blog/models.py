from django.db import models

# Create your models here.

class Post(models.Model):
    tytul = models.CharField(max_length=200)
    tresc = models.TextField()
    data_publikacji = models.DateTimeField(auto_now_add=True)
    data_modyfikacji = models.DateTimeField(auto_now=True)
    autor = models.CharField(max_length=100, default="Admin")
    opublikowany = models.BooleanField(default=True)

    def __str__(self):
        return self.tytul
