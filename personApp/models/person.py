from django.db import models
from django.db.models import Sum


class PersonQuerySet(models.QuerySet):
    def compute_dept(self):
        return (
            self.annotate(dept=Sum("transactions__price"))
            .exclude(dept=0)
            .order_by("-dept")
        )


class PersonManager(models.Manager):
    pass


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    payments = models.ManyToManyField("Payment", through="Transaction")

    objects: PersonQuerySet = PersonQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name
