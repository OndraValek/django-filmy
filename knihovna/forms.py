from django import forms
from .models import Film, Reziser, Zanr

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['nazev', 'reziseri', 'obsah', 'delka', 'rok_vydani', 'plakat', 'zanry']
        widgets = {
            'obsah': forms.Textarea(attrs={'rows': 4}),
            'delka': forms.NumberInput(attrs={'min': 1, 'max': 999}),
            'rok_vydani': forms.NumberInput(attrs={'min': 1895, 'max': 2100}),
            'reziseri': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'zanry': forms.SelectMultiple(attrs={'class': 'form-control'}),
        } 