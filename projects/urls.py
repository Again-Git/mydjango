from django.contrib import admin
from django.urls import path,include
from .views import projectsView,projectsView2,myinterface,myinterface2


urlpatterns = [
    path('projects/', projectsView.as_view()),
    path('projects/<int:pk>/',projectsView2.as_view()),
    path("interface/",myinterface.as_view()),
    path("interface/<int:pk>/",myinterface2.as_view())
]
