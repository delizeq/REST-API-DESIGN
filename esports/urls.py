from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.GameListView.as_view()),
    path('games/<int:pk>/', views.GameDetailView.as_view()),
    path('games/<int:pk>/tournaments/', views.GameTournamentsView.as_view()),

    path('teams/', views.TeamListView.as_view()),
    path('teams/<int:pk>/', views.TeamDetailView.as_view()),
    path('teams/<int:pk>/matches/', views.TeamMatchesView.as_view()),

    path('tournaments/', views.TournamentListView.as_view()),
    path('tournaments/<int:pk>/', views.TournamentDetailView.as_view()),
    path('tournaments/<int:pk>/matches/', views.TournamentMatchesView.as_view()),

    path('matches/', views.MatchListView.as_view()),
    path('matches/<int:pk>/', views.MatchDetailView.as_view()),
]