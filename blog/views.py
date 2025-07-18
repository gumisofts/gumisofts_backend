from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Author, BlogPost, Category, NewsletterSubscriber, Tag
from .serializers import (
    AuthorSerializer,
    BlogPostCreateUpdateSerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    CategorySerializer,
    NewsletterSubscriberSerializer,
    TagSerializer,
)


# Create your views here.
class NewsletterSubscriberViewset(CreateModelMixin, GenericViewSet):
    serializer_class = NewsletterSubscriberSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.select_related("author", "category").prefetch_related(
        "tags"
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "featured", "category", "tags", "author"]
    search_fields = ["title", "excerpt", "content", "author__name"]
    ordering_fields = ["published_at", "created_at", "views", "likes", "title"]
    ordering = ["-published_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogPostDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return BlogPostCreateUpdateSerializer
        return BlogPostListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # For public API, only show published posts
        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(
                status="published", published_at__lte=timezone.now()
            )

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.get_queryset().filter(featured=True)[:5]
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get posts grouped by category"""
        category_slug = request.query_params.get("category")
        if category_slug:
            posts = self.get_queryset().filter(category__slug=category_slug)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "Category parameter is required"}, status=400)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        """Like a blog post"""
        post = self.get_object()
        post.likes += 1
        post.save(update_fields=["likes"])
        return Response({"likes": post.likes})


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "bio"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
