import graphene
from graphene_django.types import DjangoObjectType
from .models import Question
from subjects.models import Subject
from users.decorators import login_required


class QuestionType(DjangoObjectType):
    class Meta:
        name = "Question"
        model = Question

    answers_count = graphene.Int(required=True)

    def resolve_answers_count(self, info):
        return self.answers.count()


class QuestionsQueries(graphene.ObjectType):
    questions = graphene.List(QuestionType, required=True)
    question = graphene.Field(QuestionType, id=graphene.ID(required=True))

    def resolve_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_question(self, info, id):
        return Question.objects.get(pk=id)


class CreateQuestionMutation(graphene.Mutation):
    class Arguments:
        subject_title = graphene.String(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    class Meta:
        name = "CreateQuestionMutationPayload"

    question = graphene.Field(QuestionType)

    @login_required
    def mutate(self, info, subject_title, title, body):
        question = Question(
            title=title, body=body, subject=Subject.objects.get(title=subject_title)
        )
        question.save()

        return CreateQuestionMutation(question=question)


class QuestionsMutations(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
