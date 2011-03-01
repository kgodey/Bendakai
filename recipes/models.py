from django.db import models
from django.contrib.auth.models import User
import datetime
from tagging.fields import TagField
import reversion


class Ingredient(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	average_rating = models.FloatField(default=0)
	equivalent_ingredients = models.ManyToManyField('self', blank=True, null=True)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name


class MeasurementUnit(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	equivalent_units = models.ManyToManyField('self', blank=True, null=True)

	def __unicode__(self):
		return self.name


class Photo(models.Model):
	image = models.ImageField(upload_to='images/')
	user = models.ForeignKey(User)


class Recipe(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	servings = models.IntegerField(blank=True, null=True, help_text='How many people might this recipe serve? Optional.')
	prep_time = models.IntegerField(blank=True, null=True, help_text='In minutes. Optional.')
	cook_time = models.IntegerField(blank=True, null=True, help_text='In minutes. Optional.')
	directions = models.TextField()
	date_added = models.DateTimeField(default=datetime.datetime.now)
	user = models.ForeignKey(User, blank=True, null=True)
	photos = models.ManyToManyField(Photo, blank=True, null=True)
	main_photos = models.ManyToManyField(Photo, blank=True, null=True, related_name='main_photos')
	is_public = models.BooleanField(default=True)
	creates_ingredient = models.ForeignKey(Ingredient, blank=True, null=True)
	source = models.TextField(blank=True, null=True, help_text='Where or from whom did you get this recipe? Optional.')
	notes = models.TextField(blank=True, null=True, help_text='Optional.')
	tags = TagField(help_text='Enclose multi word tags in double quotes and use commas to separate tags. Optional.')

	class Meta:
		ordering = ['-date_added']

	def __unicode__(self):
		return self.name
	
	@property
	def average_rating(self):
		ratings = self.ratings.all()
		if ratings:
			return sum([rating.rating for rating in ratings])/len(ratings)
		else:
			return 0


class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, related_name='ingredients')
	ingredient = models.ForeignKey(Ingredient, related_name='recipes', help_text='If entering things like "large onion", put "large" under preparation.')
	quantity = models.FloatField(null=True, blank=True, help_text='Takes fractions or decimals. Decimals below 1 must be in the form "0.x", not ".x"')
	max_quantity = models.FloatField(null=True, blank=True, help_text='For ranges of quantities e.g. "2-3 tsp".')
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)
	preparation = models.CharField(max_length=255, blank=True, null=True, help_text='Things like "to taste", "chopped", "large", "pre-cooked" etc. go here.')
	optional = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s (%s)'%(self.ingredient.name, self.recipe.name)


class JunkRecipe(models.Model):
	text = models.TextField()
	is_added = models.BooleanField()
	derived_recipe = models.ForeignKey(Recipe, blank=True, null=True)


class UserIngredientRating(models.Model):
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient, related_name='ratings')
	rating = models.IntegerField(default=0)


class UserRecipeRating(models.Model):
	user = models.ForeignKey(User)
	recipe = models.ForeignKey(Recipe, related_name='ratings')
	rating = models.IntegerField(default=0)


class PantryItem(models.Model):
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient)	
	quantity = models.FloatField(null=True, blank=True)
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)


class KitchenTool(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	user = models.ManyToManyField(User, blank=True, null=True)


class RecipeKitchenTool(models.Model):
	recipe = models.ForeignKey(Recipe, related_name = 'tools')
	tool = models.ForeignKey(KitchenTool)
	quantity = models.FloatField(null=True, blank=True, default=1)


class IngredientWeight(models.Model):
	ingredient = models.ForeignKey(Ingredient)
	unit = models.ForeignKey(MeasurementUnit)
	weight = models.FloatField()


class MeasurementConversion():
	pass


reversion.register(Ingredient)
reversion.register(MeasurementUnit)
reversion.register(Photo)
reversion.register(Recipe)
reversion.register(RecipeIngredient)
reversion.register(JunkRecipe)
reversion.register(PantryItem)
reversion.register(KitchenTool)
reversion.register(UserRecipeRating)
reversion.register(UserIngredientRating)
reversion.register(RecipeKitchenTool)
reversion.register(IngredientWeight)