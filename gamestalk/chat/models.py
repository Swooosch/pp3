""" imports """
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    This creates a custom manager. It allows us to retrieve gamechats using
    code like Gamechat.published.all()
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Gamechat.Status.PUBLISHED)

    def most_commented(self):
        return self.get_queryset().annotate(comment_count=Count(
            'comments')).order_by('-comment_count')[:3]


class Gamechat(models.Model):
    """ data model for a gamechat/post """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=210,
        unique_for_date='created_on'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_gamechats'
    )
    body = models.TextField()
    tags = TaggableManager()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    # the default manager   ie Gamechat.objects.all()
    objects = models.Manager()
    # our custom manager   ie Gamechat.published.all()
    published = PublishedManager()

    class Meta:
        """
        This class defines the meta data for the model
        ordering is tell django that it should sort results by the updated_on
        field (latest first indicated by '-')
        indexes allows us to define the database indexing for this model
        """
        ordering = ['-updated_on']
        indexes = [
            models.Index(fields=['-updated_on']),
        ]

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    def get_absolute_url(self):
        return reverse(
            "chat:gamechat_detail",
            args=[
                self.created_on.year,
                self.created_on.month,
                self.created_on.day,
                self.slug
            ]
        )

""" Model for comments on a published gamereview """

class Comment(models.Model):

    gamechat = models.ForeignKey(
        Gamechat,
        on_delete=models.CASCADE,
        related_name="chat_comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    body = models.TextField(max_length=800)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']
        indexes = [
            models.Index(fields=['created_on']),
        ]

    def __str__(self):
        return f'Comment by {self.user} on {self.gamechat}'