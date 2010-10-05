from django.contrib import admin
from .models import Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Tag, Photo


admin.site.register((Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Tag, Photo))