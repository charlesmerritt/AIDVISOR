from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('saved/', views.saved, name='saved'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('resources/', views.resources, name='resources'),
    path('api/assistant-query/', views.assistant_query, name='assistant_query'),
    path('api/save-scholarship/', views.save_scholarship, name='save_scholarship'),
    path('api/edit-user-details', views.edit_user_details, name='edit_user_details'),
]
