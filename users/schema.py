import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model, authenticate
from .utils import create_token
from .exceptions import AuthError
from .decorators import login_required

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        name = "User"
        model = User
        fields = ["username", "email", "answers"]

    answers_count = graphene.Int(required=True)

    def resolve_answers_count(self, info):
        return self.answers.count()


class UsersQueries(graphene.ObjectType):
    user = graphene.Field(UserType)

    @login_required
    def resolve_user(self, info):
        return info.context.user


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    class Meta:
        name = "CreateUserMutationPayload"

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        user.save()

        return CreateUserMutation(user=user)


class LoginMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    class Meta:
        name = "LoginMutationPayload"

    token = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        user = authenticate(info.context, username=username, password=password)

        if user is None:
            raise AuthError("please enter valid creds")

        token = create_token(user)

        return LoginMutation(token=token, user=user)


class UsersMutations(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    login = LoginMutation.Field()
