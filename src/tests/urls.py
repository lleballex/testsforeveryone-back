from django.urls import path

from . import views


urlpatterns = [
    path('', views.TestsView.as_view()),

    path('<int:id>/', views.TestView.as_view()),
    path('<int:id>/like/', views.LikeTestView.as_view()),
    path('<int:id>/dislike/', views.DislikeTestView.as_view()),

    path('own/', views.OwnTestsView.as_view()),
    path('own/<int:id>/', views.OwnTestView.as_view()),

    path('solved/', views.SolvedTestsView.as_view()),
    path('solved/<int:id>/', views.SolvedTestView.as_view()),
]