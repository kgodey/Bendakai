from django.core.management.base import BaseCommand, CommandError
from ...models import JunkRecipe
import os
from xml.etree import ElementTree as ET
from xml.parsers.expat import ExpatError

class Command(BaseCommand):
	args = 'directory_with_xml_files_in_it'
	help = 'Load junk recipes from the specified directory.'
	
	def handle(self, directory_with_xml_files_in_it=None, *args, **options):
		if directory_with_xml_files_in_it is None:
			raise CommandError('You need to provide a directory full of junk recipes to load.')
		
		all_ingredients = []

		for dirpath, dirnames, filenames in os.walk(os.path.realpath(directory_with_xml_files_in_it)):
			for d in dirnames:
				for a, b, c in os.walk(os.path.join(dirpath, d)):
					for cc in c:
						filepath = os.path.join(a, cc)
						try:
							tree = ET.parse(filepath)
						except:
							print 'An error occurred whilst trying to open %s' % filepath
						
						the_text = '\nRecipe title: %s\n' % (tree.findtext('recipe/head/title'))
						the_text += "Yields: %s serving(s)\n" % (tree.findtext("recipe/head/yield"))
						root = tree.getroot()
						categories = root.find('recipe/head/categories')
						if categories != None:
							for cat in categories:
								the_text += "Tag: %s\n" % (cat.text)
						ingredients = root.find("recipe/ingredients")
						the_text += '\nINGREDIENTS:\n\n'
						for ing in ingredients:
							if ing.find('item') != None:
								temp1 = ''
								temp2 = ''
								if ing.find('amt/qty') != None:
									temp1 = "%s " % (ing.find('amt/qty').text)
								if ing.find('amt/unit') != None:
									temp2 = "%s " % (ing.find('amt/unit').text)
								the_text += "%s%s%s\n" % (temp1, temp2, ing.find('item').text)
						the_text += '\nDIRECTIONS:\n\n'
						directions = root.find("recipe/directions")
						for step in directions:
							the_text += "%s\n" % (step.text)
					
						JunkRecipe(text=the_text, is_added=False).save()
