from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import generic
from .models import Article


def index(request):
    return HttpResponse('''Hello, world. Please go to <a href="/articles"> /articles </a>''')

class ArticleListView(generic.ListView):
    model = Article