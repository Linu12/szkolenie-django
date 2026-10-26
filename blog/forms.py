from django import forms

class KontaktForm(forms.Form):
    imie = forms.CharField(max_length=100, label='Imię')
    email = forms.EmailField(label='Email')
    wiadomosc = forms.CharField(widget=forms.Textarea, label='Wiadomość')
