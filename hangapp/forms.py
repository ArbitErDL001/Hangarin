from django.forms import ModelForm
from django import forms
from hangapp.models import Category, Note, Priority, Task, SubTask


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = "__all__"