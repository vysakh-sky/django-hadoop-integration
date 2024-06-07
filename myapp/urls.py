from django.urls import path
from .views import UpdateFileView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("articles/", views.ArticleListView.as_view(), name='Articles'),
    path('update-file/<int:id>/', UpdateFileView.as_view(), name='update-file')
]