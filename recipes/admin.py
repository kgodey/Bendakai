from django.contrib import admin
from .models import Ingredient, MeasurementUnit, Recipe, RecipeIngredient, JunkRecipe, Photo, UserRecipeRating, UserIngredientRating, PantryItem, KitchenTool, UserSavedRecipe
from reversion.admin import VersionAdmin

class RecipeAdmin(VersionAdmin):
	pass

admin.site.register((Ingredient, MeasurementUnit, RecipeIngredient, JunkRecipe, Photo, UserRecipeRating, UserIngredientRating, PantryItem, KitchenTool, UserSavedRecipe), VersionAdmin)
admin.site.register(Recipe, RecipeAdmin)