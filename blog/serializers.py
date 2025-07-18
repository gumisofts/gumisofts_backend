from rest_framework import serializers

from .models import Author, BlogPost, Category, NewsletterSubscriber, Tag


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        exclude = []
        read_only_fields = ["created_at", "updated_at"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "avatar", "bio"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class BlogPostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField(format="%Y-%m-%d")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "author",
            "published_at",
            "updated_at",
            "tags",
            "category",
            "image",
            "read_time",
            "featured",
            "likes",
            "views",
            "status",
        ]


class BlogPostDetailSerializer(BlogPostListSerializer):
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ["content"]


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "author",
            "category",
            "tags",
            "image",
            "read_time",
            "featured",
            "published_at",
            "status",
        ]
        extra_kwargs = {"slug": {"required": False}}
