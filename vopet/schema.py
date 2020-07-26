import graphene

from subjects.schema import SubjectsQueries
from questions.schema import QuestionsQueries, QuestionsMutations
from answers.schema import AnswersQueries, AnswersMutations
from users.schema import UsersQueries, UsersMutations


class Query(SubjectsQueries, QuestionsQueries, AnswersQueries, UsersQueries):
    pass


class Mutation(QuestionsMutations, AnswersMutations, UsersMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
