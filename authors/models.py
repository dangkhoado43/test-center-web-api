from django.db import models
from users.models import CustomUser

class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='authors', null=True)
    name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'authors'

    def __str__(self):
        return self.name