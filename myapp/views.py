from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import generic
from .models import Article
from django.conf import settings
import requests
from requests_gssapi import HTTPSPNEGOAuth

def index(request):
    return HttpResponse('''Hello, world. Please go to <a href="/articles"> /articles </a>''')

class ArticleListView(generic.ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hadoop_host = getattr(settings, 'HADOOP_HOST', 'localhost')
        hadoop_port = getattr(settings, 'HADOOP_PORT', 14000)
        hadoop_user = getattr(settings, 'HADOOP_USER', 'john')
        hadoop_secure = getattr(settings, 'HADOOP_SECURE', 'false')
        if hadoop_secure:
            r = requests.get(f"http://{hadoop_host}:{hadoop_port}/webhdfs/v1/?op=GETDELEGATIONTOKEN", auth=HTTPSPNEGOAuth())
            token = r.json()['Token']['urlString']
            context['auth'] = f'delegation={token}'

        else:
            context['auth'] = f'user.name={hadoop_user}'

        return context