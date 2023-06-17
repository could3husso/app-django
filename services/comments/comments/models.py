import uuid
from django.db import models

# Create your models here.
class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article_id = models.UUIDField(editable=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
   # name = models.CharField(max_length=200)
   # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title