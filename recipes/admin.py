from django.contrib import admin
from .models import Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Photo


admin.site.register((Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Photo))