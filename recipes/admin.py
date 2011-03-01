from django.contrib import admin
from .models import Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Photo, UserRecipeRating, UserIngredientRating, PantryItem, KitchenTool, RecipeKitchenTool


admin.site.register((Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Photo,  UserRecipeRating, UserIngredientRating, PantryItem, KitchenTool, RecipeKitchenTool))