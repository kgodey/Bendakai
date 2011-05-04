from django.core.management.base import BaseCommand, CommandError
from ...models import Ingredient, RecipeIngredient, Recipe, UserIngredientRating, UserRecipeRating
from django.contrib.auth.models import User
from pulp import *

class Command(BaseCommand):
	args = ''
	help = 'Solves basic linear program for a certain user'
	
	def handle(self, *args, **options):
		
		# Specifies the ID of the user (in the database) that the recommendation is for.
		USER_ID = 1
		N = 10
		C = 4000
		P = 75
		
		# Creates a list of IDs of recipes to reference.
		all_recipes = []
		for r in Recipe.objects.all():
			all_recipes.append(r.id)
		
		# Function that returns sum of ingredient and recipe ratings from the
		# specified user given its ID (pre calculated.)
		def rating(i):
			u = UserRecipeRating.objects.get(recipe__id=i, user__id=USER_ID)
			return u.total_rating
		
		# Function that returns cost of making a recipe given its ID
		def price(i):
			u = Recipe.objects.get(id=i)
			return u.price
		
		# Function that returns calories of a recipe given its ID.
		def calories(i):
			u = Recipe.objects.get(id=i)
			return u.calories
		
		# Sets up an x for every recipe, values either 0 or 1
		x = pulp.LpVariable.dicts('recipe', all_recipes, lowBound=0, upBound=1, cat=pulp.LpInteger)
		
		# Sets up the LP as a maximisation problem.
		prob = pulp.LpProblem('Recipe Recommendation Model', pulp.LpMaximize)
		
		# Adds the objective function, maximising the sum of ratings.
		prob += sum([rating(recipe) * x[recipe] for recipe in all_recipes])
		
		# Adds constraints for number of meals, calories and price.
		prob += sum(x[recipe] for recipe in all_recipes) == N, 'Total_number_of_meals_%d'%N
		prob += sum((calories(recipe) * x[recipe]) for recipe in all_recipes) <= C, 'Total_number_of_calories_%d'%C
		prob += sum((price(recipe) * x[recipe]) for recipe in all_recipes) <= P, 'Total_price_%d'%P
		
		# Calls a solving backend (GLPK in this case) to solve the problem
		prob.solve()
		
		print "Solving for user " + str(USER_ID) + " for " + str(len(all_recipes)) + " recipes."
		final_cals = 0
		final_price = 0
		final_pref = 0
		for recipe in all_recipes:
			if x[recipe].value() == 1.0:
				u = Recipe.objects.get(id=recipe)
				final_cals = final_cals + u.calories
				final_price = final_price + u.price
				final_pref = final_pref + UserRecipeRating.objects.get(recipe=u, user__id=USER_ID).total_rating
				print str(u.name) + ' | Calores: ' + str(u.calories) + ' | Price: ' + str(u.price)
		print 'Final calories: ' + str(final_cals) + ' | price: ' + str(final_price) + ' | pref: ' + str(final_pref) + ' | avg: ' + str(final_pref/N)