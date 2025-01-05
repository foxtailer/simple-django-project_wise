import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class WiseUser(AbstractUser):
  email = models.EmailField(max_length=254, unique=True)

  def __str__(self) -> str:
    return self.username
  

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    text = models.TextField(max_length=3000, null=False, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply = models.BooleanField(default=True)
    report = models.PositiveIntegerField(default=0)
    reported_by = models.ManyToManyField(WiseUser, 
                                         related_name='reported_wisdoms', 
                                         blank=True)
    accepted = models.ManyToManyField(WiseUser, 
                                      related_name='accepted', 
                                      blank=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    author = models.ForeignKey(WiseUser,
                               on_delete=models.SET_NULL,
                               related_name='wisdom',
                               null=True)
    
    objects = models.Manager()
    published = PublishedManager()

    @classmethod
    def random_wisdome(cls, except_id=None, user=None):
        if user == None:
            user = -1
            
        count = cls.published.exclude(id=except_id).exclude(reported_by__id=user).count()
        if count == 0:
            return None
        random_index = random.randint(0, count - 1)
        return cls.published.all().exclude(id=except_id).exclude(reported_by__id=user)[random_index]
