import graphene
from graphene_django.types import DjangoObjectType
from .models import Answer
from questions.models import Question
from users.decorators import login_required


class AnswerType(DjangoObjectType):
    class Meta:
        name = "Answer"
        model = Answer


class AnswersQueries(graphene.ObjectType):
    answers = graphene.List(AnswerType, required=True)

    def resolve_answers(self, info, **kwargs):
        return Answer.objects.all()


class AddAnswerMutation(graphene.Mutation):
    class Arguments:
        question_id = graphene.ID(required=True)
        body = graphene.String(required=True)

    class Meta:
        name = "AddAnswerMutationPayload"

    # The class attributes define the response of the mutation
    answer = graphene.Field(AnswerType)

    @login_required
    def mutate(self, info, question_id, body):
        answer = Answer(
            body=body,
            question=Question.objects.get(pk=question_id),
            user=info.context.user,
        )
        answer.save()

        return AddAnswerMutation(answer=answer)


class AnswersMutations(graphene.ObjectType):
    add_answer = AddAnswerMutation.Field()
