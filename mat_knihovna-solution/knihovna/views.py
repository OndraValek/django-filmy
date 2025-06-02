from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
import random

from .models import Film, Zanr, Reziser


def index(request):
    # Získání nejnovějších filmů
    nejnovejsi_filmy = Film.objects.order_by('-rok_vydani')[:5]
    
    # Získání náhodného filmu dne
    film_dne = None
    if Film.objects.exists():
        film_count = Film.objects.count()
        random_index = random.randint(0, film_count - 1)
        film_dne = Film.objects.all()[random_index]
    
    # Statistiky
    pocet_filmu = Film.objects.count()
    pocet_reziseru = Reziser.objects.count()
    
    # Získání všech žánrů pro filtrování
    zanry = Zanr.objects.annotate(pocet_filmu=Count('film')).order_by('-pocet_filmu')
    
    context = {
        'nejnovejsi_filmy': nejnovejsi_filmy,
        'film_dne': film_dne,
        'pocet_filmu': pocet_filmu,
        'pocet_reziseru': pocet_reziseru,
        'zanry': zanry,
    }
    return render(request, 'index.html', context=context)


class FilmListView(ListView):
    model = Film
    template_name = 'films/film_list.html'
    context_object_name = 'films'

    def get_queryset(self):
        queryset = Film.objects.order_by('-rok_vydani')
        
        # Vyhledávání podle názvu
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nazev__icontains=q) |
                Q(obsah__icontains=q) |
                Q(reziseri__jmeno__icontains=q) |
                Q(reziseri__prijmeni__icontains=q)
            ).distinct()
            
        # Filtrování podle žánru
        zanr = self.request.GET.get('zanr')
        if zanr:
            queryset = queryset.filter(zanry__nazev=zanr)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Přidáme informace o aktuálním vyhledávání a filtrování
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_zanr'] = self.request.GET.get('zanr', '')
        context['zanry'] = Zanr.objects.all()
        return context


class FilmDetailView(DetailView):
    model = Film
    template_name = 'films/film_detail.html'
    context_object_name = 'film'


class ReziserListView(ListView):
    model = Reziser
    context_object_name = 'reziser_list'
    queryset = Reziser.objects.annotate(pocet_filmu=Count('film')).order_by('-pocet_filmu')
    template_name = 'rezisers/reziser_list.html'


class ReziserDetailView(DetailView):
    model = Reziser
    context_object_name = 'reziser'
    template_name = 'rezisers/reziser_detail.html'
