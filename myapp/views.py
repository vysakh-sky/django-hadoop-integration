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
    
@method_decorator(require_http_methods(["PUT"]), name='dispatch')
class UpdateFileView(View):
    def put(self, request, *args, **kwargs):
        # Extract the file path and file content from the request
        file_path = request.GET.get('file_path')
        file_content = request.FILES.get('file')

        if not file_path or not file_content:
            return HttpResponseBadRequest("file_path and file are required.")

        storage = HadoopStorage()

        # Update the file in HDFS
        try:
            storage.update(file_path, file_content)
            return JsonResponse({'message': 'File updated successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)