import graphene
from graphene_django.types import DjangoObjectType
from .models import Subject


class SubjectType(DjangoObjectType):
    class Meta:
        name = "Subject"
        model = Subject


class SubjectsQueries(graphene.ObjectType):
    subjects = graphene.List(graphene.NonNull(SubjectType), required=True)
    subject = graphene.Field(SubjectType, title=graphene.String(required=True))

    def resolve_subjects(self, info, **kwargs):
        return Subject.objects.all()

    def resolve_subject(self, info, title):
        return Subject.objects.get(title=title)
