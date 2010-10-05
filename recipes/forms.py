from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import Recipe, Ingredient, RecipeIngredient
from django.contrib.auth.models import User
from django import forms


class RecipeForm(ModelForm):
	class Meta:
		model =  Recipe
		fields = ('name', 'servings', 'prep_time', 'cook_time', 'directions', 'is_public', 'creates_ingredient', 'source')


RecipeIngredientsFormset = inlineformset_factory(Recipe, RecipeIngredient)


class AddIngredientForm(ModelForm):
	class Meta:
		model = Ingredient
		exclude = ('slug',)
