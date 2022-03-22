from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    payments = models.ManyToManyField("Payment", through="Transaction")

    def __str__(self) -> str:
        return self.name
