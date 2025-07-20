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

    def create(self, request, *args, **kwargs):
        """Override create to handle duplicate subscriptions gracefully"""
        email = request.data.get("email")
        if email:
            # Check if user is already subscribed
            existing_subscriber = NewsletterSubscriber.objects.filter(
                email=email
            ).first()
            if existing_subscriber:
                if existing_subscriber.is_active:
                    return Response(
                        {
                            "message": "You are already subscribed to our newsletter!",
                            "status": "already_subscribed",
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    # Reactivate subscription
                    existing_subscriber.is_active = True
                    existing_subscriber.save()
                    return Response(
                        {
                            "message": "Your subscription has been reactivated!",
                            "status": "reactivated",
                        },
                        status=status.HTTP_200_OK,
                    )

        # Create new subscription
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.data = {
                "message": "Thank you for subscribing! Please check your email for confirmation.",
                "status": "subscribed",
            }
        return response

    @action(detail=False, methods=["post"])
    def send_newsletter(self, request):
        """Send newsletter to all active subscribers"""
        from core.emails import send_newsletter_to_subscribers

        subject = request.data.get("subject", "")
        content = request.data.get("content", "")

        if not subject:
            return Response(
                {"error": "Subject is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get featured post if provided
        featured_post_id = request.data.get("featured_post_id")
        featured_post = None
        if featured_post_id:
            try:
                blog_post = BlogPost.objects.get(
                    id=featured_post_id, status="published"
                )
                featured_post = {
                    "title": blog_post.title,
                    "excerpt": blog_post.excerpt,
                    "url": f"https://gumisofts.com/blog/{blog_post.slug}/",  # Update with actual URL
                }
            except BlogPost.DoesNotExist:
                pass

        # Get recent posts
        recent_posts_data = []
        recent_posts = BlogPost.objects.filter(status="published").order_by(
            "-published_at"
        )[:5]
        for post in recent_posts:
            recent_posts_data.append(
                {
                    "title": post.title,
                    "excerpt": post.excerpt,
                    "url": f"https://gumisofts.com/blog/{post.slug}/",  # Update with actual URL
                    "category": (
                        post.category.name if post.category else "Uncategorized"
                    ),
                    "read_time": post.read_time,
                    "published_date": (
                        post.published_at.strftime("%B %d, %Y")
                        if post.published_at
                        else ""
                    ),
                    "image": post.image.url if post.image else None,
                }
            )

        try:
            result = send_newsletter_to_subscribers(
                subject=subject,
                newsletter_content=content,
                featured_post=featured_post,
                recent_posts=recent_posts_data,
                show_stats=request.data.get("show_stats", True),
            )

            if result:
                subscriber_count = NewsletterSubscriber.objects.filter(
                    is_active=True
                ).count()
                return Response(
                    {
                        "message": f"Newsletter sent successfully to {subscriber_count} subscribers!",
                        "status": "sent",
                        "subscriber_count": subscriber_count,
                    }
                )
            else:
                return Response(
                    {
                        "message": "No active subscribers found",
                        "status": "no_subscribers",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to send newsletter: {str(e)}", "status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
