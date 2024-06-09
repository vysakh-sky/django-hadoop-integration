from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
# Create your views here.
from django.http import HttpResponse
from django.views import generic
from .models import Article
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
from requests_gssapi import HTTPSPNEGOAuth
from storage import HadoopStorage 
from django.views import View
from django.shortcuts import get_object_or_404


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

@method_decorator(require_http_methods(["POST", "GET"]), name='dispatch')
class UpdateFileView(View):
    def get(self, request, id):
        article = get_object_or_404(Article, pk=id)
        context = {
            'article': article
        }
        print(article, article.headline)
        return render(request, 'myapp/file_update.html', context=context)
 
    def post(self, request, id):
        article = get_object_or_404(Article, pk=id)

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return HttpResponseBadRequest("file is required.")

        
        old_filename = article.attachment.name

        new_filename = article.attachment.storage.save(uploaded_file.name, uploaded_file)
        article.attachment.name = new_filename
        article.save()

        article.attachment.storage.delete_signal(old_filename)

        return HttpResponse(new_filename)