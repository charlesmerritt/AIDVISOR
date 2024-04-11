from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('saved/', views.saved, name='saved'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path("create/", views.create, name="create"),
    path('resources/', views.resources, name='resources'),
    path('api/assistant-query/', views.assistant_query, name='assistant_query'),
]
