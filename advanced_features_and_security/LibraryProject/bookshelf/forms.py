from django import forms
from .models import Book  # تأكد من وجود نموذج Book في 
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']  # عدّل الحقول حسب الموجود في نموذج Book