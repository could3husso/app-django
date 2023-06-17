import uuid
from django.db import models

class Article(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200,  blank=True, default='')
    body = models.TextField()

    class Meta:
        ordering = ['created_at']


