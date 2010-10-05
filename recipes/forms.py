from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import Recipe, Ingredient, RecipeIngredient, MeasurementUnit
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import slugify


class RecipeForm(ModelForm):
	class Meta:
		model =  Recipe
		fields = ('name', 'servings', 'prep_time', 'cook_time', 'directions', 'is_public', 'source')


class RecipeIngredientForm(ModelForm):
	ingredient_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'recipeingredient_ingredient_field'}))
	unit_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'recipeingredient_unit_field'}))
	
	class Meta:
		model = RecipeIngredient
		exclude = ('ingredient', 'unit')
	
	def save(self, force_insert=False, force_update=False, commit=True):
		m = super(RecipeIngredientForm, self).save(commit=False)
		ingredient_name = self.cleaned_data['ingredient_name']
		unit_name = self.cleaned_data['unit_name']
		ingredient = Ingredient.objects.get_or_create(name__iexact=ingredient_name, defaults={'name': ingredient_name, 'slug': slugify(ingredient_name)})[0]
		unit = MeasurementUnit.objects.get_or_create(name__iexact=unit_name, defaults={'name': unit_name, 'slug': slugify(unit_name)})[0]
		m.ingredient = ingredient
		m.unit = unit
		if commit:
			m.save()
		return m


RecipeIngredientsFormset = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm)


class AddIngredientForm(ModelForm):
	class Meta:
		model = Ingredient
		exclude = ('slug',)
