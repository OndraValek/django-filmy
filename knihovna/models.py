from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Reziser(models.Model):
    jmeno = models.CharField(max_length=80, verbose_name='Jméno režiséra', help_text='Zadejte jméno režiséra',
                             error_messages={'blank': 'Jméno režiséra musí být vyplněno'})
    prijmeni = models.CharField(max_length=50, verbose_name='Příjmení režiséra', help_text='Zadejte příjmení režiséra',
                                error_messages={'blank': 'Příjmení režiséra musí být vyplněno'})
    narozeni = models.DateField(blank=True, null=True, verbose_name='Datum narození')
    umrti = models.DateField(blank=True, null=True, verbose_name='Datum úmrtí')
    biografie = models.TextField(blank=True, verbose_name='Životopis')
    fotografie = models.ImageField(upload_to='reziseri', verbose_name='Fotografie')

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Režisér'
        verbose_name_plural = 'Režiséři'

    def __str__(self):
        return f'{self.jmeno} {self.prijmeni}'


class Zanr(models.Model):
    nazev = models.CharField(max_length=20, verbose_name='Název žánru', help_text='Zadejte název žánru')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Žánr'
        verbose_name_plural = 'Žánry'

    def __str__(self):
        return f'{self.nazev}'


class Film(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název filmu', help_text='Zadejte název filmu',
                             error_messages={'blank': 'Název filmu musí být vyplněn'})
    reziseri = models.ManyToManyField(Reziser)
    obsah = models.TextField(blank=True, verbose_name='Obsah filmu', help_text='Vložte obsah filmu')
    delka = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(999)],
                                              verbose_name='Délka filmu', help_text='Zadejte délku filmu v minutách (max. 999)')
    rok_vydani = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1895), MaxValueValidator(2100)],
                                             verbose_name='Rok vydání', help_text='Zadejte rok vydání (1895 - 2100)')
    plakat = models.ImageField(upload_to='plakaty', verbose_name='Plakát filmu')
    zanry = models.ManyToManyField(Zanr)

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Film'
        verbose_name_plural = 'Filmy'

    def __str__(self):
        return f'{self.nazev} ({self.rok_vydani})'


class Recenze(models.Model):
    text = models.TextField(verbose_name='Text recenze', help_text='Vložte text recenze')
    upraveno = models.DateTimeField(verbose_name='Datum úpravy', help_text='Datum poslední úpravy', auto_now=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    recenzent = models.ForeignKey(User, on_delete=models.CASCADE)

    class Hodnoceni(models.IntegerChoices):
        NULA = 0, ''
        JEDNA = 1, '*'
        DVA = 2, '**'
        TRI = 3, '***'
        CTYRI = 4, '****'
        PET = 5, '*****'

    hodnoceni = models.IntegerField(default=3, choices=Hodnoceni.choices)

    class Meta:
        ordering = ['-hodnoceni']
        verbose_name = 'Recenze'
        verbose_name_plural = 'Recenze'

    def __str__(self):
        return f'{self.recenzent.last_name if self.recenzent.last_name else self.recenzent}: {self.text}, hodnocení: {self.hodnoceni}, ({self.upraveno.strftime("%Y-%m-%d %H:%M:%S")})'
