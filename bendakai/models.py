from django.db import models
from django.contrib.auth.models import User
import datetime
from taggit.managers import TaggableManager

class Ingredient(models.Model):
	"""
	A class that models an ingredient (independent of recipe.)
	
	"""

	name = models.CharField(max_length=255)
	slug = models.SlugField()
	# Ingredients that should be considered the same as this one.
	equivalent_ingredients = models.ManyToManyField('self', blank=True, null=True)
	pantry_users = models.ManyToManyField(User, blank=True, null=True, related_name='pantry_items')

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name


class MeasurementUnit(models.Model):
	"""
	A class that models a unit (independent of recipe.)
	
	"""

	name = models.CharField(max_length=255)
	slug = models.SlugField()
	# Units that should be considered the same as this one.
	equivalent_units = models.ManyToManyField('self', blank=True, null=True)

	def __unicode__(self):
		return self.name


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
	starred_by = models.ManyToManyField(User, blank=True, null=True, related_name='starred_recipe_set')
	
	class Meta:
		ordering = ['-date_added']
	
	def __unicode__(self):
		return self.title


class RecipeIngredient(models.Model):
	"""
	A class that maps recipes to ingredients.
	
	"""
	recipe = models.ForeignKey(Recipe, related_name='ingredients')
	ingredient = models.ForeignKey(Ingredient, related_name='recipes', help_text='If entering things like "large onion", put "large" under description.')
	min_quantity = models.CharField(max_length=255, null=True, blank=True, help_text='Takes fractions or decimals. Decimals below 1 must be in the form "0.x", not ".x"')
	max_quantity = models.FloatField(null=True, blank=True, help_text='For ranges of quantities e.g. "2-3 tsp".')
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)
	description = models.CharField(max_length=255, blank=True, null=True, help_text='Things like "diced", "large", "pre-cooked", "ripe" etc. go here.')
	optional = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s (%s)'%(self.ingredient.name, self.recipe.name)



class UserIngredientRating(models.Model):
	"""
	A class that stores user ratings for ingredients.
	"""

	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient, related_name='ratings')
	rating = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s rates %s %d stars'%(self.user.username, self.ingredient.name, self.rating)


class UserRecipeRating(models.Model):
	"""
	A class that stores user ratings for recipes.
	
	"""
	user = models.ForeignKey(User)
	recipe = models.ForeignKey(Recipe, related_name='ratings')
	rating = models.IntegerField(default=0)
	
	def __unicode__(self):
		return '%s rates "%s" %d stars'%(self.user.username, self.recipe.name, self.rating)