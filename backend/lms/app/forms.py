from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth.models import User

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'isbn', 'category']

class IssueBookForm(forms.Form):
    student_id = forms.CharField(max_length=100)
    isbn = forms.CharField(max_length=13)

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class PasswordChangeForm(BasePasswordChangeForm):
    class Meta:
        model = User