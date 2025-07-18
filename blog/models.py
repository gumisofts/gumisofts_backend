from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="authors/", blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(
        max_length=500, help_text="Brief description of the post"
    )
    content = RichTextField(help_text="Main content of the blog post")

    # Relationships
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="blog_posts"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="blog_posts")

    # Media
    image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        help_text="Featured image for the post",
    )

    # Metadata
    read_time = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        help_text="Estimated reading time in minutes",
    )
    featured = models.BooleanField(default=False, help_text="Mark as featured post")
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Status
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == "published" and self.published_at is not None
