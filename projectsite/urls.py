from django.contrib import admin
from django.urls import path
from hangapp.views import (HomePageView, 
CategoryList, NoteList, 
CategoryCreateView, NoteCreateView, 
CategoryUpdateView, NoteUpdateView, 
CategoryDeleteView, NoteDeleteView)
from hangapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    #Listview
    path('category_list', CategoryList.as_view(), name='category-list'),
    path('note_list', NoteList.as_view(), name='note-list'),
    #Createview
    path('category_list/add', CategoryCreateView.as_view(), name='category-add'),
    path('note_list/add', NoteCreateView.as_view(), name='note-add'),
    #Updateview
    path('category_list/<pk>',CategoryUpdateView.as_view(), name='category-update'),
    path('note_list/<pk>', NoteUpdateView.as_view(), name='note-update'),
    #Deleteview
    path('category_list/<pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('note_list/<pk>/delete', NoteDeleteView.as_view(), name='note-delete'),
]