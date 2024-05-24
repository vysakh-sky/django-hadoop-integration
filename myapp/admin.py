from django.contrib import admin
from .models import Article
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display=('headline', 'attachment')
    
admin.site.register(Article, ArticleAdmin)
