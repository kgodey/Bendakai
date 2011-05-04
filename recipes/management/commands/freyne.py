from django.core.management.base import BaseCommand, CommandError
from recipes.models import Recipe, Ingredient, UserIngredientRating, UserRecipeRating
from django.contrib.auth.models import User
import operator

class Command(BaseCommand):
	# args = ''
	# help = ''
	
	def handle(self, *args, **options):
		# if condition is true:
		# 	raise CommandError('Error name here')

		# Implementing the recommendation systems in the Freyne & Berkovsky paper.

		def mean_user(user, use_recipes=True, use_ingredients=True):
			"""
			Returns the mean user rating of the user provided.
	
			Keyword arguments:
			user -- The user for whom the mean rating is to be calculated.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the mean rating calculation.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the mean rating calculation.
	
			"""
			total_rating = 0
			num = 0
			if use_recipes:
				for rating in UserRecipeRating.objects.filter(user = user):
					total_rating += rating.rating
					num += 1
			if use_ingredients:
				for rating in UserIngredientRating.objects.filter(user = user):
					total_rating += rating.rating
					num += 1
			return total_rating/num


		def user_similarity(user1, user2, use_recipes=False, use_ingredients=False):
			"""
			Returns the similarity score of two users.
	
			Keyword arguments:
			user1 -- The first user that is being compared.
			user2 -- The second user that is being compared.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the similarity metric.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the similarity metric.
	
			"""
			numerator = 0
			denominator_1 = 0
			denominator_2 = 0
			mean_user1 = mean_user(user1)
			mean_user2 = mean_user(user2)
			if use_recipes:
				recipes_with_ratings = Recipe.objects.filter(ratings__user = user1).filter(ratings__user = user2)
				for recipe in recipes_with_ratings:
					user1_rating = UserRecipeRating.objects.get(recipe = recipe, user = user1).rating
					user2_rating = UserRecipeRating.objects.get(recipe = recipe, user = user2).rating
					numerator = numerator + (user1_rating - mean_user1)*(user2_rating - mean_user2)
					denominator_1 = denominator_1 + (user1_rating - mean_user1)**2
					denominator_2 = denominator_2 + (user2_rating - mean_user2)**2
			if use_ingredients:
				ingredients_with_ratings = Ingredient.objects.filter(ratings__user = user1).filter(ratings__user = user2)
				for ingredient in ingredients_with_ratings:
					user1_rating = UserIngredientRating.objects.get(ingredient = ingredient, user = user1).rating
					user2_rating = UserIngredientRating.objects.get(ingredient = ingredient, user = user2).rating
					numerator = numerator + (user1_rating - mean_user1)*(user2_rating - mean_user2)
					denominator_1 = denominator_1 + (user1_rating - mean_user1)**2
					denominator_2 = denominator_2 + (user2_rating - mean_user2)**2
			return numerator/(denominator_1*denominator_2)


		def find_similar_users(user1, num_users=10, use_recipes=False, use_ingredients=False):
			"""
			Returns a list of similar users to the user provided.
	
			Keyword arguments:
			user1 -- The user for whom similar users are being calculated.
			num_users -- The number of similar users to return.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the similarity metric.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the similarity metric.
	
			"""
			users = []
			user_scores = {}
			for user2 in User.objects.all():
				if use_recipes and use_ingredients:
					user_scores[user2] = user_similarity(user1, user2, True, True)
				elif use_recipes:
					user_scores[user2] = user_similarity(user1, user2, True, False)
				elif use_ingredients:
					user_scores[user2] = user_similarity(user1, user2, False, True)
			sorted_x = sorted(user_scores.iteritems(), key=operator.itemgetter(1), reverse=True)
			for x in sorted_x[:num]:
				users.append(x[1])
			return users


		def prediction(user, recipe):
			"""
			Returns a predicted rating for a given recipe by the given user.
	
			Keyword arguments:
			user -- The user for whom the rating is being predicted.
			recipe -- The recipe for which the rating is being predicted.
	
			"""
			total_rating = 0
			num_ingredients = 0
			for ingredient in recipe.ingredients.ingredient.all():
				rating = ingredient.ratings(user = user).rating
				total_rating = total_rating + rating
				num_ingredients += 1
			return total_rating / num_ingredients




		def rating_method1(user1, ingredient):
			"""
			Returns a predicted rating for a given ingredient by the given user.
	
			Keyword arguments:
			user1 -- The user for whom the rating is being predicted.
			ingredient -- The ingredient for which the rating is being predicted.
	
			"""
			numerator = 0
			denominator = 0
			users = find_similar_users_r(user1)
			for user in users:
				if UserIngredientRating.objects.filter(user = user, ingredient = ingredient):
					rating = UserIngredientRating.objects.filter(user = user, ingredient = ingredient).rating
				else:
					rating = 0
				numerator = numerator + user_sim_ingredients(user, user1)*rating
				denominator = denominator + user_sim_ingredients(user, user1)
			return numerator/denominator
			

		def rating_method2(user1, ingredient):
			"""
			Returns a predicted rating for a given ingredient by the given user.
	
			Keyword arguments:
			user1 -- The user for whom the rating is being predicted.
			ingredient -- The ingredient for which the rating is being predicted.
	
			"""
			numerator = 0
			recipes = Recipe.objects.filter(ratings__user = user1).filter(ingredients__ingredient = ingredient)
			l = len(recipes)
			for recipe in recipes:
				numerator = numerator + UserRecipeRating.objects.filter(recipe = recipe, user = user1)
			return numerator/l
			
		
		# Testing functions code.	
		user1 = User.objects.get(id=1)
		user2 = User.objects.get(id=19)
		print mean_user(user1, True, False), mean_user(user2, True, False)