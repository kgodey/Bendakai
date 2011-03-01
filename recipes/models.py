from django.db import models
from django.contrib.auth.models import User
import datetime
from tagging.fields import TagField 	#new

#delete this model and use django-tagging
#class Tag(models.Model):
#	name = models.CharField(max_length=255)
#	slug = models.SlugField()


class Ingredient(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	average_rating = models.FloatField(default=0)	#new #TODO: insert validators to make sure it is between 1-5
	equivalent_ingredients = models.ManyToManyField('self', blank=True, null=True)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name


class MeasurementUnit(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
#	weight = models.FloatField(blank=True, null=True)
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

class UserIngredientRating(models.Model): #new
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient, related_name='ratings')
	rating = models.IntegerField(default=0)	#TODO: insert validators to make sure it is an integer or integer and a half between 1 and 5

class UserRecipeRating(models.Model): #new
	user = models.ForeignKey(User)
	recipe = models.ForeignKey(Recipe, related_name='ratings')
	rating = models.IntegerField(default=0)	#TODO: insert validators to make sure it is an integer or integer and a half between 1 and 5

class PantryItem(models.Model):	#new
	user = models.ForeignKey(User)
	ingredient = models.ForeignKey(Ingredient)	
	quantity = models.FloatField(null=True, blank=True)
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)

class KitchenTool(models.Model): #new
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	user = models.ManyToManyField(User, blank=True, null=True)

class RecipeKitchenTool(models.Model): #new
	recipe = models.ForeignKey(Recipe, related_name = 'tools')
	tool = models.ForeignKey(KitchenTool)
	quantity = models.FloatField(null=True, blank=True, default=1)

class IngredientWeight():	#new
	ingredient = models.ForeignKey(Ingredient)
	unit = models.ForeignKey(MeasurementUnit)
	weight = models.FloatField()

class MeasurementConversion():	#new
	pass

##35 reviews
##38 comments
#40 nutritional data association
##43 tags
##51 ranges
##56 associate similar ingredient names, units
##57 notes field on recipe
##59 correct recipe feature
##60 user pantry
##61 kitchen tools