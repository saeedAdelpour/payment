import graphene
from graphene_django import DjangoObjectType

from .models import Person


class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = "__all__"


class PersonAppQuery:
    persons = graphene.List(PersonType)

    def resolve_persons(parent, info):
        return Person.objects.all()


class CreatePersonMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    person = graphene.Field(PersonType)
    created = graphene.Boolean()

    def mutate(self, info, name):
        person, created = Person.objects.get_or_create(name=name)
        return CreatePersonMutation(person=person, created=created)


class PersonAppMutation:
    create_person = CreatePersonMutation.Field()
