from django import forms
from fractions import Fraction

class FractionField(forms.RegexField):
	def __init__(self, *args, **kwargs):
		super(FractionField, self).__init__(r'^((?:\d+\.?\d*/?\d*)(?: \d+/\d+)?)$', *args, **kwargs)
	
	def to_python(self, value):
		value = super(FractionField, self).to_python(value)
		split_value = value.split(' ')
		if len(split_value) > 1:
			fraction_float = float(Fraction(split_value[1]))
			return float(split_value[0]) + fraction_float
		elif len(split_value) == 1:
			return float(Fraction(split_value[0]))
		return float(value) if value else None