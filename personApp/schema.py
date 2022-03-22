import graphene
from graphene_django import DjangoObjectType

from django.db import transaction

from .models import Person, Payment, Transaction


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ["id", "person", "payment", "price", "created_at", "status"]


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ["id", "name"]


class PersonAppQuery:
    persons = graphene.List(PersonType)

    def resolve_persons(parent, info):
        return Person.objects.all()


class PaymentQuery(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ["id", "description", "created_at"]


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
