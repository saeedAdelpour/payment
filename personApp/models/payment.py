from django.db import models


class Payment(models.Model):
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.description}"
