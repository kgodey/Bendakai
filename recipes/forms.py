from django import forms
from models import Recipe, Ingredient, RecipeIngredient, MeasurementUnit, KitchenTool, UserKitchenTool
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from fields import FractionField
from tagging.fields import TagField

class RecipeForm(forms.ModelForm):
	"""
	A class that defines the form for recipe submission.
	
	"""
	
	tools = forms.CharField(required=False, help_text=Recipe._meta.get_field('tools').help_text, widget=forms.TextInput(attrs={'class': 'recipe_tools'}))
	
	class Meta:
		"""
		A class that defines the properties of the form, including
		which model to use for creation and which fields to include
		from it.
		
		"""
		
		model = Recipe
		fields = ('name', 'servings', 'prep_time', 'cook_time', 'directions', 'is_public', 'source', 'notes', 'tags')
	
	def save(self, commit=True):
		"""
		An overwrite of the form save method that parses the tools
		added.
		
		Keyword arguments:
		self -- the RecipeForm instance
		commit -- whether the changes to the form should be committed
		
		"""
		
		m = super(RecipeForm, self).save(commit=False)
		# Parsing the "tools" field in the form
		tools = str(self.cleaned_data['tools']).split(',')
		for tool_name in tools:
			if tool_name != '':
				tool, created = KitchenTool.objects.get_or_create(name=tool_name, defaults={'slug': slugify(tool_name)})
				tool.save()
				m.tools.add(tool)
		if commit:
			m.save()
		return m


class RecipeIngredientForm(forms.ModelForm):
	"""
	A class that defines the form for submission of ingredients
	associated with a recipe.
	
	"""
	
	ingredient_name = forms.CharField(help_text=RecipeIngredient._meta.get_field('ingredient').help_text, widget=forms.TextInput(attrs={'class': 'recipeingredient_ingredient_field'}))
	quantity = FractionField(required=False, help_text=RecipeIngredient._meta.get_field('quantity').help_text,widget=forms.TextInput(attrs={'class': 'recipeingredient_quantity_field'}))
	max_quantity = FractionField(required=False, help_text=RecipeIngredient._meta.get_field('max_quantity').help_text, widget=forms.TextInput(attrs={'class': 'recipeingredient_max_quantity_field'}))
	unit_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'recipeingredient_unit_field'}))
	
	class Meta:
		"""
		A class that defines the properties of the form, including
		which model to use for creation and which fields to include
		from it.
		
		"""
		
		model = RecipeIngredient
		exclude = ('ingredient', 'unit')
		fields = ('ingredient_name', 'quantity', 'max_quantity', 'unit_name', 'preparation', 'optional')
	
	def save(self, commit=True):
		"""
		An overwrite of the form save method that parses the ingredients,
		units and optional fields.
		
		Keyword arguments:
		self -- the RecipeIngredientForm instance
		commit -- whether the changes to the form should be committed
		
		"""
		
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
		"""
		An overwrite of the form's initialisation methods that prepopulate
		the ingredient and unit fields if the data is available.
		
		Keyword arguments:
		self -- the RecipeIngredientForm instance
		
		"""
		
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

RecipeIngredientsFormset = forms.models.inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm)