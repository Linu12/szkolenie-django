from django.db import models
# Create your models here.
class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa
    class Meta:
        verbose_name_plural = "Kategorie"

class Tag(models.Model):
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return self.nazwa
    class Meta:
        verbose_name_plural = "Tagi"



class Post(models.Model):
    tytul = models.CharField(max_length=200)
    tresc = models.TextField()
    data_publikacji = models.DateTimeField(auto_now_add=True)
    data_modyfikacji = models.DateTimeField(auto_now=True)
    autor = models.CharField(max_length=100, default="Admin")
    opublikowany = models.BooleanField(default=True)
    kategoria = models.ForeignKey(
        Kategoria,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="posty"
    )
    tagi = models.ManyToManyField(Tag, blank=True, related_name='posty')

    def __str__(self):
        return self.tytul


