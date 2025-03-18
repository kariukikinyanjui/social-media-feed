import graphene
from graphene_django.types import DjangoObjectType
from core.models import User
from posts.models imoprt Post
from interactions.models import Comment, Like, Share


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, World!")

schema = graphene.Schema(query=Query)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture', 'bio')


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'image', 'timestamp', 'likes_count', 'comments_count', 'shares_count')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'timestamp')


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ('id', 'post', 'user', 'timestamp')


class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = ('id', 'post', 'user', 'timestamp')
