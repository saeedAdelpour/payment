from django.db import models
from django.utils.translation import gettext_lazy as _
from .payment import Payment


class TransactionManager(models.Manager):
    def create_transaction(self, description, price, persons, paid_person):
        price_each = price / len(persons) * -1
        payment = Payment.objects.create(description=description)
        persons_must_pay = list(filter(lambda _id: _id != paid_person, persons))

        transactions = []
        for person_id in persons_must_pay:
            transactions.append(
                self.model(
                    person_id=person_id,
                    payment=payment,
                    price=price_each,
                    status=self.model.TransactionStatusChoices.pending,
                )
            )

        pay_value_for_paid_person = -1 * len(persons_must_pay) * price_each
        transactions.append(
            self.model(
                person_id=paid_person,
                payment=payment,
                price=pay_value_for_paid_person,
                status=self.model.TransactionStatusChoices.pending,
            )
        )
        return self.bulk_create(transactions)


class Transaction(models.Model):
    class TransactionStatusChoices(models.TextChoices):
        pending = "pending", _("Pending")
        paid = "paid", _("Paid")

    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="transactions"
    )
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TransactionStatusChoices.choices, max_length=20)

    objects: TransactionManager = TransactionManager()
