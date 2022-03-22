import graphene

from personApp.schema import PersonAppQuery, PersonAppMutation


class Query(PersonAppQuery, graphene.ObjectType):
    pass


class Mutation(PersonAppMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
