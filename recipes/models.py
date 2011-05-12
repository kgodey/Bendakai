from django.db import models
from django.contrib.auth.models import User
from nutrition.models import Food
import datetime
from tagging.fields import TagField
import reversion


class Ingredient(models.Model):
	"""
	A class that models an ingredient (independent of recipe.)
	
	"""
	
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	average_rating = models.FloatField(default=0)
	#	Ingredients that should be considered the same as this one.
	equivalent_ingredients = models.ManyToManyField('self', blank=True, null=True)
	#	Mapping to a food in the nutrition database.
	food = models.ForeignKey(Food, blank=True, null=True)

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
	#	Units that should be considered the same as this one.
	equivalent_units = models.ManyToManyField('self', blank=True, null=True)

	def __unicode__(self):
		return self.name


class Photo(models.Model):
	"""
	A class that models an image.
	
	"""
	
	image = models.ImageField(upload_to='images/')
	#	The owner of this image.
	user = models.ForeignKey(User)


class KitchenTool(models.Model):
	"""
	A class that models a kitchen tool i.e. a blender or a
	potato masher.
	
	"""
	
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name


class Recipe(models.Model):
	"""
	A class that models a recipe.
	
	"""
	
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	servings = models.IntegerField(blank=True, null=True, help_text='How many people might this recipe serve? Optional.')
	prep_time = models.IntegerField(blank=True, null=True, help_text='In minutes. Optional.')
	cook_time = models.IntegerField(blank=True, null=True, help_text='In minutes. Optional.')
	directions = models.TextField()
	date_added = models.DateTimeField(default=datetime.datetime.now)
	user = models.ForeignKey(User, blank=True, null=True)
	photos = models.ManyToManyField(Photo, blank=True, null=True)
	#	Photos that should be displayed more prominently.
	main_photos = models.ManyToManyField(Photo, blank=True, null=True, related_name='main_photos')
	is_public = models.BooleanField(default=True)
	#	For instance, a recipe for "ketchup" can be linked to that ingredient.
	creates_ingredient = models.ForeignKey(Ingredient, blank=True, null=True)
	source = models.TextField(blank=True, null=True, help_text='Where or from whom did you get this recipe? Optional.')
	notes = models.TextField(blank=True, null=True, help_text='Optional.')
	tags = TagField(help_text='Enclose multi word tags in double quotes and use commas to separate tags. Optional.')
	tools = models.ManyToManyField(KitchenTool, blank=True, null=True)

	class Meta:
		ordering = ['-date_added']

	def __unicode__(self):
		return self.name
	
	@property
	def average_rating(self):
		"""
		Calculates average rating of the recipe.
		
		Keyword arguments:
		self -- the Recipe instance for which ratings are calculated.

		"""
		
		ratings = self.ratings.all()
		if ratings:
			return sum([rating.rating for rating in ratings])/len(ratings)
		else:
			return 0


class RecipeIngredient(models.Model):
	"""
	A class that maps recipes to ingredients.
	
	"""
	
	recipe = models.ForeignKey(Recipe, related_name='ingredients')
	ingredient = models.ForeignKey(Ingredient, related_name='recipes', help_text='If entering things like "large onion", put "large" under preparation.')
	quantity = models.FloatField(null=True, blank=True, help_text='Takes fractions or decimals. Decimals below 1 must be in the form "0.x", not ".x"')
	max_quantity = models.FloatField(null=True, blank=True, help_text='For ranges of quantities e.g. "2-3 tsp".')
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)
	#	Encompasses things such as "fresh", "ripe", "mashed", "diced", "large" etc.
	preparation = models.CharField(max_length=255, blank=True, null=True, help_text='Things like "to taste", "chopped", "large", "pre-cooked" etc. go here.')
	#	Whether the ingredient is optional for the recipe.
	optional = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s (%s)'%(self.ingredient.name, self.recipe.name)


class JunkRecipe(models.Model):
	"""
	A class that models a plaintext recipe.
	
	"""
	
	text = models.TextField()
	is_added = models.BooleanField()
	derived_recipe = models.ForeignKey(Recipe, blank=True, null=True)


class UserIngredientRating(models.Model):
	"""
	A class that stores user ratings for ingredients.
	
	"""
	
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient, related_name='ratings')
	rating = models.IntegerField(default=0)
	
	def __unicode__(self):
		return '%s - %s'%(self.user.username, self.ingredient.name)


class UserRecipeRating(models.Model):
	"""
	A class that stores user ratings for recipes.
	
	"""
	
	user = models.ForeignKey(User)
	recipe = models.ForeignKey(Recipe, related_name='ratings')
	rating = models.IntegerField(default=0)
	
	def __unicode__(self):
		return '%s - %s'%(self.user.username, self.recipe.name)


class PantryItem(models.Model):
	"""
	A class that stores ingredients in user's pantries.
	
	"""
	
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient)	
	quantity = models.FloatField(null=True, blank=True)
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)
	
	def __unicode__(self):
		return '%s - %s'%(self.user.username, self.ingredient.name)


class IngredientWeight(models.Model):
	"""
	A class that maps ingredient units to weights.
	
	"""
	
	ingredient = models.ForeignKey(Ingredient)
	unit = models.ForeignKey(MeasurementUnit)
	weight = models.FloatField()
	
	def __unicode__(self):
		return '%f - %s'%(self.weight, self.ingredient.name)


class UserSavedRecipe(models.Model):
	"""
	A class that stores recipes saved by users.
	
	"""
	
	user = models.ForeignKey(User, related_name='saved_recipes')
	recipe = models.ForeignKey(Recipe, related_name='saved_users')
	date_added = models.DateTimeField(default=datetime.datetime.now)
	
	def __unicode__(self):
		return '%s - %s'%(self.user.username, self.recipe.name)


class UserKitchenTool(models.Model):
	"""
	A class that stores kitchen tools that users own.
	
	"""
	
	user = models.ForeignKey(User, related_name='tools')
	tool = models.ForeignKey(KitchenTool, related_name='users')
	quantity = models.IntegerField(blank=True, null=True, default=1)
	
	def __unicode__(self):
		return '%s - %s'%(self.user.username, self.tool.name)


class MeasurementConversion():
	"""
	A class that will store conversions between various
	measurements of ingredients.
	
	"""
	
	pass

reversion.register(Ingredient)
reversion.register(MeasurementUnit)
reversion.register(Photo)
reversion.register(Recipe)
reversion.register(RecipeIngredient)
reversion.register(JunkRecipe)
reversion.register(PantryItem)
reversion.register(KitchenTool)
reversion.register(UserKitchenTool)
reversion.register(UserRecipeRating)
reversion.register(UserIngredientRating)
reversion.register(IngredientWeight)
reversion.register(UserSavedRecipe)