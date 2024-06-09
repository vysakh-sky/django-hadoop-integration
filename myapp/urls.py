from django.urls import path
from .views import UpdateFileView
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", views.index, name="index"),
    path("articles/", views.ArticleListView.as_view(), name='Articles'),
    path('update-file/<int:id>/', csrf_exempt(UpdateFileView.as_view()), name='update-file')
]