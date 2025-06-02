from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('films', views.FilmListView.as_view(), name='films_list'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
    path('rezisers', views.ReziserListView.as_view(), name='rezisers_list'),
    path('reziser/<int:pk>/', views.ReziserDetailView.as_view(), name='reziser_detail'),
]
