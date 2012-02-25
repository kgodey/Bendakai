from django.db import models
from django.contrib.auth.models import User
import datetime
from taggit.managers import TaggableManager


class Recipe(models.Model):
    """
    A class that models a recipe.
    
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField()
    directions = models.TextField()
    servings = models.IntegerField(blank=True, null=True)
    prep_time = models.IntegerField(blank=True, null=True)
    cook_time = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    tags = TaggableManager()
    date_added = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User, blank=True, null=True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __unicode__(self):
        return self.title