from django.contrib import admin
from .models import FoodGroup, Food, Nutrient, Source, Derivation, DataSource, NutrientValue, Weight, Footnote


class WeightInline(admin.TabularInline):
	model = Weight


class FootnoteInline(admin.TabularInline):
	model = Footnote


class NutrientValueInline(admin.TabularInline):
	model = NutrientValue
	fk_name = 'food'


class FoodAdmin(admin.ModelAdmin):
	list_display = ('description', 'short_description', 'scientific_name', 'food_group', 'ndb_number')
	list_filter = ('food_group', 'manufacturer', 'fndds_profile')
	search_fields = ('description', 'short_description', 'scientific_name')
	inlines = [NutrientValueInline] #WeightInline, FootnoteInline]
#	the above line is commented out because this will cause the server to run out of memory :\
#	in other words, don't uncomment it


admin.site.register(Food, FoodAdmin)
admin.site.register((Nutrient, Source, Derivation, DataSource))
