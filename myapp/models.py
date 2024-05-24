from django.db import models
from storage import HadoopStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=100)
    attachment = models.FileField(storage=HadoopStorage())

    def __str__(self):
        return f'{self.headline} - {self.attachment}'
    
@receiver(post_delete, sender=Article)
def delete_article_image(sender, instance, **kwargs):
    try:
        instance.attachment.storage.delete_signal(instance.attachment.name)
    except:
        print(f"Deletion of {instance.attachment.name} failed in signal!")