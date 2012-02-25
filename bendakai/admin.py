from django.contrib import admin
from .models import Recipe, UserRecipeRating, PantryItem

admin.site.register((Recipe, UserRecipeRating, PantryItem), admin.ModelAdmin)