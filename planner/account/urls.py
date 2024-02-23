# account/urls.py
from django.urls import path
from . import views
from .views import add_category, add_note, update_note, edit_category, delete_category, edit_note, delete_note


urlpatterns = [
    path('', views.profile, name="profile"),
    path('notes/', views.notes, name='notes'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/', edit_category, name='edit_category'),
    path('delete_category/', delete_category, name='delete_category'),
    path('add_note/', add_note, name='add_note'),
    path('update_note/', update_note, name='update_note'),
    path('edit_note/', edit_note, name='edit_note'),
    path('delete_note/', delete_note, name='delete_note'),

]