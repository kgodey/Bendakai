from django.core.management.base import BaseCommand, CommandError
from ...models import FoodGroup, Food, Nutrient, Source, Derivation, DataSource, NutrientValue, Weight, Footnote
from decimal import Decimal
import os
import csv

csv.register_dialect('usda', delimiter='^', quotechar='~')

class Command(BaseCommand):
	args = 'sr##_dir'
	help = 'Load the USDA National Nutrient Database for Standard Reference from the specified directory.'
	
	def handle(self, path=None, *args, **options):
		if path is None:
			raise CommandError('You must provide a directory to load the data files from.')
		
		path = os.path.realpath(path)
		
		try:
			FOOD_DES = csv.reader(open(os.path.join(path, 'FOOD_DES.txt'), 'rb'), 'usda')
			FD_GROUP = csv.reader(open(os.path.join(path, 'FD_GROUP.txt'), 'rb'), 'usda')
			NUT_DATA = csv.reader(open(os.path.join(path, 'NUT_DATA.txt'), 'rb'), 'usda')
			NUTR_DEF = csv.reader(open(os.path.join(path, 'NUTR_DEF.txt'), 'rb'), 'usda')
			SRC_CD = csv.reader(open(os.path.join(path, 'SRC_CD.txt'), 'rb'), 'usda')
			DERIV_CD = csv.reader(open(os.path.join(path, 'DERIV_CD.txt'), 'rb'), 'usda')
			WEIGHT = csv.reader(open(os.path.join(path, 'WEIGHT.txt'), 'rb'), 'usda')
			FOOTNOTE = csv.reader(open(os.path.join(path, 'FOOTNOTE.txt'), 'rb'), 'usda')
			DATSRCLN = csv.reader(open(os.path.join(path, 'DATSRCLN.txt'), 'rb'), 'usda')
			DATA_SRC = csv.reader(open(os.path.join(path, 'DATA_SRC.txt'), 'rb'), 'usda')
		except:
			raise CommandError('An error occurred while trying to read a data file.')
		else:
			self.load_fd_group(FD_GROUP)
			self.load_food_des(FOOD_DES)
			self.load_nutr_def(NUTR_DEF)
			self.load_src_cd(SRC_CD)
			self.load_deriv_cd(DERIV_CD)
			self.load_data_src(DATA_SRC)
			self.load_nut_data(NUT_DATA)
			self.load_weight(WEIGHT)
			self.load_footnote(FOOTNOTE)
			self.load_datsrcln(DATSRCLN)
	
	def load_fd_group(self, FD_GROUP):
		for line in FD_GROUP:
			line = self.parse_line(line)
			try:
				food_group = FoodGroup.objects.get(code=line[0])
			except:
				food_group = FoodGroup()
				food_group.code = line[0]
			food_group.name = line[1]
			food_group.save()
	
	def load_food_des(self, FOOD_DES):
		for line in FOOD_DES:
			line = self.parse_line(line)
			try:
				food = Food.objects.get(ndb_number=line[0])
			except:
				food = Food()
				food.ndb_number = line[0]
			food.food_group = FoodGroup.objects.get(code=line[1])
			food.description = line[2]
			food.short_description = line[3]
			food.other_names = line[4]
			food.manufacturer = line[5]
			food.fndds_profile = self.parse_boolean(line[6])
			food.inedible_parts_description = line[7]
			food.inedible_parts_percentage = line[8]
			food.scientific_name = line[9]
			food.nitrogen_to_protein_factor = line[10]
			food.protein_to_calories_factor = line[11]
			food.fat_to_calories_factor = line[12]
			food.carb_to_calories_factor = line[13]
			food.save()
	
	def load_nutr_def(self, NUTR_DEF):
		for line in NUTR_DEF:
			line = self.parse_line(line)
			try:
				nutrient = Nutrient.objects.get(number=line[0])
			except:
				nutrient = Nutrient()
				nutrient.number = line[0]
			nutrient.units = line[1]
			nutrient.tagname = line[2]
			nutrient.name = line[3]
			nutrient.value_decimal_places = line[4]
			nutrient.sr_order = line[5]
			nutrient.save()
	
	def load_src_cd(self, SRC_CD):
		for line in SRC_CD:
			line = self.parse_line(line)
			try:
				source = Source.objects.get(code=line[0])
			except:
				source = Source()
				source.code = line[0]
			source.description = line[1]
			source.save()
	
	def load_deriv_cd(self, DERIV_CD):
		for line in DERIV_CD:
			line = self.parse_line(line)
			try:
				derivation = Derivation.objects.get(code=line[0])
			except:
				derivation = Derivation()
				derivation.code = line[0]
			derivation.description = line[1]
			derivation.save()
	
	def load_data_src(self, DATA_SRC):
		for line in DATA_SRC:
			line = self.parse_line(line)
			try:
				data_source = DataSource.objects.get(datasrc_id=line[0])
			except:
				data_source = DataSource()
				data_source.datasrc_id = line[0]
			data_source.authors = line[1]
			data_source.title = line[2] or ''
			data_source.year = line[3]
			data_source.journal = line[4]
			data_source.vol_city = line[5]
			data_source.issue_state = line[6]
			data_source.start_page = line[7]
			data_source.end_page = line[8]
			data_source.save()
	
	def load_nut_data(self, NUT_DATA):
		for line in NUT_DATA:
			line = self.parse_line(line)
			food = Food.objects.get(ndb_number=line[0])
			nutrient = Nutrient.objects.get(number=line[1])
			try:
				nutrient_value = NutrientValue.objects.get(food=food, nutrient=nutrient)
			except:
				nutrient_value = NutrientValue()
				nutrient_value.food = food
				nutrient_value.nutrient = nutrient
			nutrient_value.value = line[2]
			nutrient_value.data_points = line[3]
			nutrient_value.standard_error = line[4]
			nutrient_value.source = Source.objects.get(code=line[5])
			if line[6] is not None:
				nutrient_value.derivation = Derivation.objects.get(code=line[6])
			else:
				nutrient_value.derivation = None
			if line[7] is not None:
				nutrient_value.inferred_from = Food.objects.get(ndb_number=line[7])
			else:
				nutrient_value.inferred_from = None
			nutrient_value.added = self.parse_boolean(line[8])
			nutrient_value.studies = line[9]
			nutrient_value.minimum = line[10]
			nutrient_value.maximum = line[11]
			nutrient_value.degrees_of_freedom = line[12]
			nutrient_value.lower_error_bound = line[13]
			nutrient_value.upper_error_bound = line[14]
			nutrient_value.statistical_comments = line[15]
			nutrient_value.confidence_code = line[16]
			nutrient_value.save()
	
	def load_weight(self, WEIGHT):
		for line in WEIGHT:
			line = self.parse_line(line)
			food = Food.objects.get(ndb_number=line[0])
			seq = line[1]
			try:
				weight = Weight.objects.get(food=food, sequence_number=seq)
			except:
				weight = Weight()
				weight.food = food
				weight.sequence_number = seq
			weight.amount = line[2]
			weight.description = line[3]
			weight.grams = line[4]
			weight.data_points = line[5]
			weight.standard_deviation = line[6]
			weight.save()
	
	def load_footnote(self, FOOTNOTE):
		# this one is tricky, so it just adds them without trying to find them first
		for line in FOOTNOTE:
			line = self.parse_line(line)
			footnote = Footnote()
			footnote.food = Food.objects.get(ndb_number=line[0])
			footnote.number = line[1]
			footnote.footnote_type = line[2]
			if line[3] is not None:
				footnote.nutrient = Nutrient.objects.get(number=line[3])
			else:
				footnote.nutrient = None
			footnote.text = line[4]
			footnote.save()
	
	def load_datsrcln(DATSRCLN):
		for line in DATSRCLN:
			line = self.parse_line(line)
			food = Food.objects.get(ndb_number=line[0])
			nutrient = Nutrient.objects.get(number=line[1])
			data_source = DataSource.objects.get(datasrc_id=line[2])
			nutrient_value = NutrientValue.objects.get(food=food, nutrient=nutrient)
			nutrient_value.data_sources.add(data_source)
			nutrient_value.save()
	
	def parse_line(self, line):
		""" Replaces blank strings with None objects """
		parsed = []
		for field in line:
			if len(field) == 0:
				field = None
			parsed.append(field)
		return parsed
	
	def parse_boolean(self, value):
		if value is not None:
			if value == 'Y':
				return True
			else:
				return False
		return None