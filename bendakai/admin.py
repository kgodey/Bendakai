from django.contrib import admin
from .models import Recipe, UserRecipeRating, Ingredient, UserIngredientRating, RecipeIngredient, MeasurementUnit

admin.site.register((Recipe, UserRecipeRating, Ingredient, UserIngredientRating, RecipeIngredient, MeasurementUnit), admin.ModelAdmin)