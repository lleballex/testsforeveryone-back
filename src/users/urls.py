from django.urls import path

from . import views


urlpatterns = [
    path('signin/', views.SignInView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('<str:username>/', views.UserView.as_view()),
]