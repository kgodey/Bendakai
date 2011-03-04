from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import Recipe, Ingredient, RecipeIngredient, MeasurementUnit, KitchenTool, UserKitchenTool
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import slugify
from fields import FractionField

class RecipeForm(ModelForm):
	tools = forms.CharField(required=False, help_text=Recipe._meta.get_field('tools').help_text, widget=forms.TextInput(attrs={'class': 'recipe_tools'}))
	
	class Meta:
		model =  Recipe
		fields = ('name', 'servings', 'prep_time', 'cook_time', 'directions', 'is_public', 'source', 'notes', 'tags')
	
	def save(self, force_insert=False, force_update=False, commit=True):
		m = super(RecipeForm, self).save(commit=False)
		tools = str(self.cleaned_data['tools']).split(',')
		for tool_name in tools:
			if tool_name != '':
				tool, created = KitchenTool.objects.get_or_create(name=tool_name, defaults={'slug': slugify(tool_name)})
				tool.save()
				m.tools.add(tool)
			if commit:
				m.save()
			return m


class RecipeIngredientForm(ModelForm):
	ingredient_name = forms.CharField(help_text=RecipeIngredient._meta.get_field('ingredient').help_text, widget=forms.TextInput(attrs={'class': 'recipeingredient_ingredient_field'}))
	quantity = FractionField(required=False, help_text=RecipeIngredient._meta.get_field('quantity').help_text,widget=forms.TextInput(attrs={'class': 'recipeingredient_quantity_field'}))
	max_quantity = FractionField(required=False, help_text=RecipeIngredient._meta.get_field('max_quantity').help_text, widget=forms.TextInput(attrs={'class': 'recipeingredient_max_quantity_field'}))
	unit_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'recipeingredient_unit_field'}))
	
	class Meta:
		model = RecipeIngredient
		exclude = ('ingredient', 'unit')
		fields = ('ingredient_name', 'quantity', 'max_quantity', 'unit_name', 'preparation', 'optional')
	
	def save(self, force_insert=False, force_update=False, commit=True):
		m = super(RecipeIngredientForm, self).save(commit=False)
		ingredient_name = self.cleaned_data['ingredient_name']
		unit_name = self.cleaned_data['unit_name']
		optional = self.cleaned_data['optional']
		ingredient = Ingredient.objects.get_or_create(name__iexact=ingredient_name, defaults={'name': ingredient_name, 'slug': slugify(ingredient_name)})[0]
		unit = MeasurementUnit.objects.get_or_create(name__iexact=unit_name, defaults={'name': unit_name, 'slug': slugify(unit_name)})[0]
		m.ingredient = ingredient
		m.unit = unit
		m.optional = optional
		if commit:
			m.save()
		return m
	
	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)
		initial = kwargs.pop('initial', None)
		if instance is not None:
			if initial is None:
				initial = {}
				initial['ingredient_name'] = instance.ingredient.name
				initial['unit_name'] = instance.unit.name
			if initial is not None:
				kwargs['initial'] = initial
		super(RecipeIngredientForm, self).__init__(*args, **kwargs)


RecipeIngredientsFormset = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm)


class AddIngredientForm(ModelForm):
	class Meta:
		model = Ingredient
		exclude = ('slug',)

class SearchForm(forms.Form):
	searchterm = forms.CharField()