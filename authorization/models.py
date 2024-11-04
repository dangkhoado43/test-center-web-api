from django.db import models
from users.models import CustomUser

class Session(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"

class RevokedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    revoked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revoked Token: {self.token}"