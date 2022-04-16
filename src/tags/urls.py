from django.urls import path

from . import views


urlpatterns = [
    path('', views.TagsView.as_view()),
]