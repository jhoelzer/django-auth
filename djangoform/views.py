from django.shortcuts import render, reverse, HttpResponseRedirect
from djangoform.models import Recipes, Author
from djangoform.forms import AuthorForm, RecipeForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def list_view(request):
    html = 'list_view.html'
    items = Recipes.objects.all().order_by('title')
    return render(request, html, {'list': items})


@login_required()
def create_recipe(request):
    html = 'create_recipe.html'
    form = None
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipes.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time=data['time'],
                instructions=data['instructions'],
            )
        return render(request, 'created_recipe.html')
    else:
        form = RecipeForm()
    return render(request, html, {'form': form})


def recipe_info(request, id):
    html = 'recipe_info.html'
    items = Recipes.objects.all().filter(id=id)
    instructions = items[0].instructions.split('\n')
    return render(request, html,
                  {'recipes': items, 'instructions': instructions})


@login_required()
@staff_member_required()
def create_author(request):
    html = 'create_author.html'
    form = None
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            login(request, user)
            Author.objects.create(
                name=data['name'],
                bio=data['bio'],
                user=user
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AuthorForm()
    return render(request, html, {'form': form})


def author_info(request, id):
    html = 'author_info.html'
    authors = Author.objects.all().filter(id=id)
    items = Recipes.objects.all().filter(author_id=id)
    return render(request, html, {'authors': authors, 'recipes': items})


def login_view(request):
    html = 'login_view.html'
    form = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully logged out')
    return HttpResponseRedirect(reverse('homepage'))
