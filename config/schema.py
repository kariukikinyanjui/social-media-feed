import graphene
from graphene_django.types import DjangoObjectType
from core.models import User
from posts.models imoprt Post
from interactions.models import Comment, Like, Share


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.ID(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

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
