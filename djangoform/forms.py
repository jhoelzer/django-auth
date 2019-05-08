from django import forms
from djangoform.models import Author


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=500)
    username = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=200)
    time = forms.CharField(max_length=100)
    instructions = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
