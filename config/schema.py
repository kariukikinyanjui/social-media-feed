import graphene
from graphene_django.types import DjangoObjectType
from core.models import User
from posts.models import Post
from interactions.models import Comment, Like, Share


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


class PostInput(graphene.InputObjectType):
    content = graphene.String(required=True)
    image = graphene.String()


class CommentInput(graphene.InputObjectType):
    post_id = graphene.ID(required=True)
    text = graphene.String(required=True)


class LikeInput(graphene.InputObjectType):
    post_id = graphene.ID(required=True)


class ShareInput(graphene.InputObjectType):
    post_id = graphene.ID(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        post = Post(
            author=user,
            content=input.content,
            image=input.image,
        )
        post.save()
        return CreatePOst(post=post)


class LikePost(graphene.Mutation):
    class Arguments:
        input = LikeInput(required=True)

    like = graphene.Field(LikeType)

    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        post = Post.objects.get(id=input.post_id)
        like, created = Like.objects.get_or_create(post=post, user=user)
        if created:
            post.likes_count += 1
            post.save()
        return LikePost(like=like)


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        post = Post.objects.get(id=input.post_id)
        comment = Comment(
            post=post,
            user=user,
            text=input.text,
        )
        comment.save()
        post.comments_count += 1
        post.save()
        return CreateComment(comment=comment)


class SharePost(graphene.Mutation):
    class Arguments:
        input = ShareInput(required=True)

    share = graphene.Field(ShareType)

    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        post = Post.objects.get(id=input.post_id)
        share = Share(post=post, user=user)
        share.save()
        post.shares_count += 1
        post.save()
        return SharePost(share=share)


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_posts = graphene.List(PostType)
    all_likes = graphene.List(LikeType)
    all_shares = graphene.List(ShareType)
    post_by_id = graphene.Field(PostType, id=graphene.ID(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_all_likes(root, info):
        return Like.objects.all()

    def resolve_all_shares(root, info):
        return Share.objects.all()

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
