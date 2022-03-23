from django.db import models
from django.db.models import Sum


class PersonQuerySet(models.QuerySet):
    def compute_debt(self):
        return (
            self.annotate(debt=Sum("transactions__price"))
            .exclude(debt=0)
            .order_by("-debt")
        )


class PersonManager(models.Manager):
    pass


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    payments = models.ManyToManyField("Payment", through="Transaction")

    objects: PersonQuerySet = PersonQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name
