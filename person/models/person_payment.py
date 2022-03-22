from django.db import models
from django.utils.translation import gettext_lazy as _


class personPayment(models.Model):
    class personPaymentStatusChoices(models.TextChoices):
        pending = "pending", _("Pending")
        paid = "paid", _("Paid")

    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=personPaymentStatusChoices.choices, max_length=20)
