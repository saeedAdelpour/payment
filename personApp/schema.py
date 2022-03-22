import graphene
from graphene_django import DjangoObjectType

from django.db import transaction

from .models import Person, Payment, Transaction


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ["id", "person", "payment", "price", "created_at", "status"]


class PersonType(DjangoObjectType):
    dept = graphene.Float()

    class Meta:
        model = Person
        fields = ["id", "name"]


class ComputePaymentType(graphene.ObjectType):
    debtor = graphene.Field(PersonType)
    creditor = graphene.Field(PersonType)
    price = graphene.Float()


class PersonAppQuery:
    persons = graphene.List(PersonType)
    compute_payments = graphene.List(ComputePaymentType)

    def resolve_persons(parent, info):
        return Person.objects.all()

    def resolve_compute_payments(parent, info):
        persons = list(Person.objects.all().compute_dept())
        creditors = list(filter(lambda p: p.dept > 0, persons))
        debtors = list(filter(lambda p: p.dept < 0, persons))

        transactions = []
        for creditor in creditors:
            for debtor in debtors:
                price = min(abs(debtor.dept), abs(creditor.dept))
                if price == 0:
                    continue
                transactions.append(
                    ComputePaymentType(debtor=debtor, creditor=creditor, price=price)
                )
                debtor.dept += price

        return transactions


class CreatePersonMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    person = graphene.Field(PersonType)
    created = graphene.Boolean()

    def mutate(self, info, name):
        person, created = Person.objects.get_or_create(name=name)
        return CreatePersonMutation(person=person, created=created)


class CreateTransactionMutation(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        price = graphene.Float()
        persons = graphene.List(graphene.ID)
        paid_person = graphene.ID()

    succes = graphene.Boolean()

    @transaction.atomic
    def mutate(self, info, description, price, persons, paid_person):
        Transaction.objects.create_transaction(
            description,
            price,
            persons,
            paid_person,
        )

        return CreateTransactionMutation(succes=True)


class PersonAppMutation:
    create_person = CreatePersonMutation.Field()
    create_transaction = CreateTransactionMutation.Field()
