from django.db import models
from django.contrib.auth.models import User

class TODOS(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marked = models.BooleanField(default=False)

