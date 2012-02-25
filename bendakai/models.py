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
    owner = models.ForeignKey(User, blank=True, null=True)
    starred_by = models.ManyToManyField(User, blank=True, null-True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __unicode__(self):
        return self.title


class UserRecipeRating(models.Model):
    """
    A class that stores user ratings for recipes.
    
    """
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='ratings')
    rating = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '%s rates "%s" %d stars'%(self.user.username, self.recipe.name, self.rating)


class PantryItem(models.Model):
    """
    A class that stores an item in the users' pantry.
    
    """
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, blank=True, null=True)