from django.db import models
from storage import HadoopStorage

# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=100)
    attachment = models.FileField(storage=HadoopStorage())

    def __str__(self):
        return f'{self.headline} - {self.attachment}'