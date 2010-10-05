# -*- coding: utf-8 -*-
from django.db import models


class FoodGroup(models.Model): # FD_GROUP
	code = models.CharField(max_length=4, unique=True, help_text='4-digit code identifying a food group. Only the first 2 digits are currently assigned. In the future, the last 2 digits may be used. Codes may not be consecutive.')
	name = models.CharField(max_length=60)
	
	def __unicode__(self):
		return self.name


class Food(models.Model): # FOOD_DES
	ndb_number = models.CharField(max_length=5, unique=True, help_text='5-digit Nutrient Databank number.')
	food_group = models.ForeignKey(FoodGroup, related_name='foods')
	description = models.CharField(max_length=200)
	short_description = models.CharField(max_length=60)
	
	other_names = models.CharField(max_length=100, null=True, blank=True, help_text='Other names commonly used to describe a food, including local or regional names for various foods, for example, “soda” or “pop” for “carbonated beverages.”')
	manufacturer = models.CharField(max_length=65, null=True, blank=True)
	fndds_profile = models.NullBooleanField(blank=True, help_text='Indicates if the food item is used in the USDA Food and Nutrient Database for Dietary Studies (FNDDS) and thus has a complete nutrient profile for the 65 FNDDS nutrients.')
	inedible_parts_description = models.CharField(max_length=135, null=True, blank=True, help_text='Description of inedible parts of a food item (refuse), such as seeds or bone.')
	inedible_parts_percentage = models.IntegerField(null=True, blank=True, help_text='Percentage of refuse.')
	scientific_name = models.CharField(max_length=65, null=True, blank=True, help_text='Scientific name of the food item. Given for the least processed form of the food (usually raw), if applicable.')
	
	nitrogen_to_protein_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='Factor for converting nitrogen to protein.')
	protein_to_calories_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from protein.')
	fat_to_calories_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from fat.')
	carb_to_calories_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from carbohydrate.')
	
	def __unicode__(self):
		return self.description


class Nutrient(models.Model): # NUTR_DEF
	number = models.CharField(max_length=3, unique=True, help_text='Unique 3-digit identifier code for a nutrient.')
	units = models.CharField(max_length=7, help_text='Units of measure (mg, g, μg, and so on).')
	tagname = models.CharField(max_length=20, null=True, blank=True, help_text='International Network of Food Data Systems (INFOODS) Tagnames.[INFOODS, 2009.] A unique abbreviation for a nutrient/food component developed by INFOODS to aid in the interchange of data.')
	name = models.CharField(max_length=60)
	value_decimal_places = models.IntegerField(max_length=1, help_text='Number of decimal places to which a nutrient value is rounded.')
	sr_order = models.IntegerField(max_length=6, help_text='Used to sort nutrient records in the same order as various reports produced from SR.')
	
	def __unicode__(self):
		return self.name


class Source(models.Model): # SRC_CD
	code = models.CharField(max_length=2, unique=True, help_text='2-digit code.')
	description = models.CharField(max_length=60)


class Derivation(models.Model): # DERIV_CD
	code = models.CharField(max_length=4, unique=True, help_text='Derivation Code.')
	description = models.CharField(max_length=120, help_text='Description of derivation code giving specific information on how the value was determined.')


class DataSource(models.Model): # DATA_SRC
	datasrc_id = models.CharField(max_length=6, unique=True, help_text='Unique number identifying the reference/source.')
	authors = models.CharField(max_length=255, null=True, blank=True, help_text='List of authors for a journal article or name of sponsoring organization for other documents.')
	title = models.CharField(max_length=255, help_text='Title of article or name of document, such as a report from a company or trade association.')
	year = models.IntegerField(max_length=4, null=True, blank=True, help_text='Year article or document was published.')
	journal = models.CharField(max_length=135, null=True, blank=True, help_text='Name of the journal in which the article was published.')
	vol_city = models.CharField(max_length=16, null=True, blank=True, help_text='Volume number for journal articles, books, or reports; city where sponsoring organization is located.')
	issue_state = models.CharField(max_length=5, null=True, blank=True, help_text='Issue number for journal article; State where the sponsoring organization is located.')
	start_page = models.IntegerField(max_length=5, null=True, blank=True, help_text='Starting page number of article/document.')
	end_page = models.IntegerField(max_length=5, null=True, blank=True, help_text='Ending page number of article/document.')


class NutrientValue(models.Model): # NUT_DATA
	food = models.ForeignKey(Food, related_name='nutrient_values')
	nutrient = models.ForeignKey(Nutrient)
	value = models.DecimalField(max_digits=10, decimal_places=3, help_text='Amount in 100 grams, edible portion.')
	data_points = models.IntegerField(max_length=5, help_text='The number of analyses (sample size) used to calculate the nutrient value. If the number of data points is 0, the value was calculated or imputed.')
	standard_error = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, help_text='Standard error of the mean. Null if can not be calculated.')
	source = models.ForeignKey(Source, help_text='Code indicating type of data.')
	
	derivation = models.ForeignKey(Derivation, null=True, blank=True, help_text='Data Derivation Code giving specific information on how the value is determined.')
	inferred_from = models.ForeignKey(Food, null=True, blank=True, help_text='NDB number of the item used to impute a missing value. Populated only for items added or updated starting with SR14.', related_name='influenced_nutrient_values')
	added = models.NullBooleanField(blank=True, help_text='Indicates a vitamin or mineral added for fortification or enrichment. This field is populated for ready-to-eat breakfast cereals in food group 8.')
	studies = models.IntegerField(max_length=2, null=True, blank=True, help_text='Number of studies.')
	minimum = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text='Minimum value.')
	maximum = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text='Maximum value.')
	degrees_of_freedom = models.IntegerField(max_length=2, null=True, blank=True)
	lower_error_bound = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text='Lower 95% error bound.')
	upper_error_bound = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text='Upper 95% error bound.')
	statistical_comments = models.CharField(max_length=10, null=True, blank=True)
	confidence_code = models.CharField(max_length=1, null=True, blank=True, help_text='Confidence Code indicating data quality, based on evaluation of sample plan, sample handling, analytical method, analytical quality control, and number of samples analyzed.')
	
	data_sources = models.ManyToManyField(DataSource, related_name='nutrient_values')
	
	class Meta:
		unique_together = ('food', 'nutrient')


class Weight(models.Model): # WEIGHT
	food = models.ForeignKey(Food, related_name='weights')
	sequence_number = models.CharField(max_length=2)
	amount = models.DecimalField(max_digits=5, decimal_places=3, help_text='Unit modifier (for example, 1 in “1 cup”).')
	description = models.CharField(max_length=80, help_text='Description (for example, cup, diced, and 1-inch pieces).')
	grams = models.DecimalField(max_digits=7, decimal_places=1, help_text='Gram weight.')
	data_points = models.IntegerField(max_length=3, null=True, blank=True)
	standard_deviation = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
	
	class Meta:
		unique_together = ('food', 'sequence_number')


class Footnote(models.Model): # FOOTNOTE
	FOOTNOTE_TYPE_CHOICES = (
		('D', 'footnote adding information to the food description'),
		('M', 'footnote adding information to measure description'),
		('N', 'footnote providing additional information on a nutrient value')
	)
	food = models.ForeignKey(Food, related_name='footnotes')
	number = models.CharField(max_length=4, help_text='Sequence number. If a given footnote applies to more than one nutrient number, the same footnote number is used.')
	footnote_type = models.CharField(max_length=1, choices=FOOTNOTE_TYPE_CHOICES)
	nutrient = models.ForeignKey(Nutrient, null=True, blank=True)
	text = models.CharField(max_length=200)
