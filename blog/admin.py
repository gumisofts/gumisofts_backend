from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Author, BlogPost, Category, NewsletterSubscriber, Tag, Topic


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "get_avatar_preview", "get_posts_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "bio"]
    readonly_fields = ["created_at", "updated_at"]

    def get_avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "No Avatar"

    get_avatar_preview.short_description = "Avatar"

    def get_posts_count(self, obj):
        count = obj.blog_posts.count()
        url = reverse("admin:blog_blogpost_changelist") + f"?author__id__exact={obj.id}"
        return format_html('<a href="{}">{} posts</a>', url, count)

    get_posts_count.short_description = "Posts"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_posts_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at"]

    def get_posts_count(self, obj):
        count = obj.blog_posts.count()
        url = (
            reverse("admin:blog_blogpost_changelist") + f"?category__id__exact={obj.id}"
        )
        return format_html('<a href="{}">{} posts</a>', url, count)

    get_posts_count.short_description = "Posts"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_posts_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at"]

    def get_posts_count(self, obj):
        count = obj.blog_posts.count()
        return f"{count} posts"

    get_posts_count.short_description = "Posts"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "status",
        "featured",
        "get_image_preview",
        "views",
        "likes",
        "published_at",
    ]
    list_filter = [
        "status",
        "featured",
        "category",
        "tags",
        "author",
        "published_at",
        "created_at",
    ]
    search_fields = ["title", "excerpt", "content", "author__name"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    readonly_fields = ["views", "likes", "created_at", "updated_at"]
    date_hierarchy = "published_at"

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "excerpt", "content")}),
        ("Relationships", {"fields": ("author", "category", "tags")}),
        ("Media & Settings", {"fields": ("image", "read_time", "featured")}),
        ("Publishing", {"fields": ("status", "published_at")}),
        ("Statistics", {"fields": ("views", "likes"), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    actions = ["make_published", "make_draft", "make_featured"]

    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "No Image"

    get_image_preview.short_description = "Image"

    def make_published(self, request, queryset):
        updated = queryset.update(status="published", published_at=timezone.now())
        self.message_user(request, f"{updated} posts were published.")

    make_published.short_description = "Mark selected posts as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} posts were moved to draft.")

    make_draft.short_description = "Mark selected posts as draft"

    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} posts were marked as featured.")

    make_featured.short_description = "Mark selected posts as featured"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


# Customize admin site header and title
admin.site.site_header = "Blog Admin"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to Blog Administration"
