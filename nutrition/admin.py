from django.contrib import admin
from .models import FoodGroup, Food, Nutrient, Source, Derivation, DataSource, NutrientValue, Weight, Footnote


class WeightInline(admin.TabularInline):
	model = Weight
	fk_name = 'food'


class NutrientValueInline(admin.TabularInline):
	model = NutrientValue
	fk_name = 'food'
	readonly_fields = ('nutrient', 'source', 'derivation', 'inferred_from', 'data_sources')


class FoodAdmin(admin.ModelAdmin):
	list_display = ('description', 'short_description', 'scientific_name', 'food_group', 'ndb_number')
	list_filter = ('food_group', 'manufacturer', 'fndds_profile')
	search_fields = ('description', 'short_description', 'scientific_name')
	inlines = [NutrientValueInline, WeightInline]


admin.site.register(Food, FoodAdmin)
admin.site.register((Nutrient, Source, Derivation, DataSource))
