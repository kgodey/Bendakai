from django import forms
from fractions import Fraction
import re

class FractionField(forms.RegexField):
	"""
	A class that converts fractional input into floats for storage.
	
	"""
	
	def __init__(self, *args, **kwargs):
		super(FractionField, self).__init__(r'^((?:\d+\.?\d*/?\d*)(?: \d+/\d+)?)$', *args, **kwargs)
	
	def to_python(self, value):
		"""
		Coerces the fractional input into a float. Matches input in the set 
		[x, x/y, x y/z] where x, y, z are decimal numbers.
		
		Keyword arguments:
		self -- the FractionField instance on which this method is called.
		value -- the value to be converted into a float.
		
		"""
		
		if value == '':
			return None
		else:
			value = super(FractionField, self).to_python(value)
			regex = r'^((?:\d+\.?\d*/?\d*)(?: \d+/\d+)?)$'
			matches_regex = re.match(regex, value)
			if matches_regex:
				split_value = value.split(' ')
				if len(split_value) > 1:
					fraction_float = float(Fraction(split_value[1]))
					return float(split_value[0]) + fraction_float
				elif len(split_value) == 1:
					return float(Fraction(split_value[0]))
				return float(value)
			else:
				return value
