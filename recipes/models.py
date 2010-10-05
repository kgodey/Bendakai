from django.db import models
from django.contrib.auth.models import User
import datetime

class Tag(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()


class Ingredient(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name


class MeasurementUnit(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	weight = models.FloatField(blank=True, null=True)
	
	def __unicode__(self):
		return self.name


class Photo(models.Model):
	image = models.ImageField(upload_to='images/')
	user = models.ForeignKey(User)


class Recipe(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	servings = models.IntegerField(blank=True, null=True, help_text="How many people might this recipe serve?")
	prep_time = models.IntegerField(blank=True, null=True, help_text="In minutes.")
	cook_time = models.IntegerField(blank=True, null=True, help_text="In minutes.")
	directions = models.TextField()
	date_added = models.DateTimeField(default=datetime.datetime.now)
	user = models.ForeignKey(User)
	photos = models.ManyToManyField(Photo, blank=True, null=True)
	main_photos = models.ManyToManyField(Photo, blank=True, null=True, related_name="main_photos")
	is_public = models.BooleanField(default=True)
	creates_ingredient = models.ForeignKey(Ingredient, blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True, null=True)
	source = models.TextField(blank=True, null=True)
	
	class Meta:
		ordering = ['date_added']
	
	def __unicode__(self):
		return self.name

class RecipeIngredient(models.Model):
	recipe = models.ForeignKey(Recipe, related_name='ingredients')
	ingredient = models.ForeignKey(Ingredient)
	preparation = models.CharField(max_length=255, blank=True, null=True)
	optional = models.BooleanField(default=False)
	quantity = models.FloatField(null=True, blank=True)
	unit = models.ForeignKey(MeasurementUnit, null=True, blank=True)


class JunkRecipe(models.Model):
	text = models.TextField()
	is_added = models.BooleanField()
