from django.core.management.base import BaseCommand, CommandError
from recipes.models import Recipe, Ingredient, UserIngredientRating, UserRecipeRating, RecipeIngredient
from django.contrib.auth.models import User
import operator

###########################################
### This code is currently experimental ###
### and very inefficient. Please don't  ###
### use it for practical purposes.      ###
###########################################

class Command(BaseCommand):
	args = 'username'
	help = 'Finds recipes to recommend based on the Freyne/Berkovsky paper.'
	
	def handle(self, username=None, *args, **options):
		if username is None:
			raise CommandError('You need to provide a username.')
		try: 
			recommendation_user = User.objects.get(username = username)
		except User.DoesNotExist:
		 	raise CommandError('User not found.')
		
		# Implementing the recommendation systems in the Freyne & Berkovsky paper.
		
		USER_SIMILARITY = {}
		self.SIMILAR_USERS = []
			
			
		def mean_user(user, use_recipes=True, use_ingredients=True):
			print 'Finding mean for user ' + user.username
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
			if num == 0:
				return num
			else:
				return total_rating/num


		def user_similarity(user1, user2, use_recipes=True, use_ingredients=True):
			"""
			Returns the similarity score of two users.
	
			Keyword arguments:
			user1 -- The first user that is being compared.
			user2 -- The second user that is being compared.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the similarity metric.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the similarity metric.
	
			"""
			try:
				return USER_SIMILARITY[(user1, user2, use_recipes, use_ingredients)]
			except:
				print 'Finding similarity between users ' + user1.username + ' ' + user2.username
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
				if denominator_1 == 0 or denominator_2 == 0:
					USER_SIMILARITY[(user1, user2, use_recipes, use_ingredients)] = 0
					return 0
				else:
					USER_SIMILARITY[(user1, user2, use_recipes, use_ingredients)] = numerator/(denominator_1*denominator_2)
					return numerator/(denominator_1*denominator_2)


		def find_similar_users(user1, num_users=10, use_recipes=True, use_ingredients=True):
			"""
			Returns a list of similar users to the user provided.
			
			Keyword arguments:
			user1 -- The user for whom similar users are being calculated.
			num_users -- The number of similar users to return.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the similarity metric.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the similarity metric.
			
			"""
			if len(self.SIMILAR_USERS) > 0:
				return self.SIMILAR_USERS
			else:
				print 'Finding similar users to ' + user1.username
				users = []
				user_scores = {}
				for user2 in User.objects.all():
					user_scores[user2] = int(user_similarity(user1, user2, use_recipes, use_ingredients))
				sorted_x = sorted(user_scores.iteritems(), key=operator.itemgetter(1), reverse=True)
				for x in sorted_x[:num_users]:
					users.append(x[0])
				self.SIMILAR_USERS = users
				return users


		def rating_method1(user1, ingredient, use_recipes=True, use_ingredients=True):
			print 'Finding rating for ' + user1.username + ' and ' + ingredient.name.encode('ascii','ignore')
			"""
			Returns a predicted rating for a given ingredient by the given user.
	
			Keyword arguments:
			user1 -- The user for whom the rating is being predicted.
			ingredient -- The ingredient for which the rating is being predicted.
			use_recipes -- A boolean signifying whether recipe ratings should be used in the similarity metric.
			use_ingredients -- A boolean signifying whether ingredient ratings should be used in the similarity metric.
	
			"""
			numerator = 0
			denominator = 0
			users = find_similar_users(user1, 10, use_recipes, use_ingredients)
			for user in users:
				try:
					rating = UserIngredientRating.objects.get(user = user, ingredient = ingredient).rating
				except:
					rating = 0
				numerator = numerator + user_similarity(user, user1, use_recipes, use_ingredients)*rating
				denominator = denominator + user_similarity(user, user1, use_recipes, use_ingredients)
			if denominator == 0:
				return denominator
			else:
				return numerator/denominator
			

		def rating_method2(user1, ingredient):
			print 'Finding rating for ' + user1.username + ' and ' + ingredient.name.encode('ascii','ignore')
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
				numerator = numerator + UserRecipeRating.objects.get(recipe = recipe, user = user1).rating
			if l == 0:
				return l
			else:
				return numerator/l
		
		
		def prediction(user1, recipe, method='ri'):
			print 'Finding prediction for ' + user1.username + ' and ' + recipe.name.encode('ascii','ignore')
			"""
			Returns a predicted rating for a given recipe by the given user.

			Keyword arguments:
			user1 -- The user for whom the rating is being predicted.
			recipe -- The recipe for which the rating is being predicted.
			method -- A string containing which rating method to use for predictions. Acceptable values are 'ri', 'r', 'i', 2'.

			"""
			total_rating = 0
			num_ingredients = 0
			for ingredient in Ingredient.objects.filter(recipes__recipe=recipe):
				try:
					rating = UserIngredientRating.objects.get(user=user1, ingredient=ingredient).rating
				except:
					if method == 'ri':
						rating = rating_method1(user1, ingredient, True, True)
					elif method == 'i':
						rating = rating_method1(user1, ingredient, False, True)
					elif method == 'r':
						rating = rating_method1(user1, ingredient, True, False)
					elif method == '2':
						rating = rating_method2(user1, ingredient)
					else:
						raise CommandError('Rating method provided incorrect. Must be ri, r, i or 2.')
				total_rating = total_rating + rating
				num_ingredients += 1
			if num_ingredients == 0:
				return num_ingredients
			else:
				return total_rating / num_ingredients
		
		
		def predict_recipes(user, method='ri'):
			print 'Finding recipes for ' + user.username + ' using ' + method
			"""
			Returns predicted recipe ratings for all recipes.

			Keyword arguments:
			user -- The user for whom the ratings is being predicted.
			method -- A string containing which rating method to use for predictions. Acceptable values are 'ri', 'r', 'i', 2'.

			"""
			user_recipe_ratings = {}
			for recipe in Recipe.objects.all():
				try:
					user_recipe_ratings[recipe] = UserRecipeRating.objects(user=user, recipe=recipe).rating
				except:
					user_recipe_ratings[recipe] = prediction(user, recipe, method)
			return user_recipe_ratings
		
		
		def test_algorithms(user, num_recipes=20):
			print 'Testing algorithm.'
			predictions = []
			final_recipes = []
			for method in ['ri', 'i', 'r', '2']:
				predictions.append(predict_recipes(user, method))
			for prediction in predictions:
				sorted_predictions = sorted(prediction.iteritems(), key=operator.itemgetter(1), reverse=True)
				final_recipes.append(sorted_predictions[:num_recipes])
			return final_recipes

		# Calculates 20 most recommended recipes for user. Can be refined according to calories etc.
		print test_algorithms(recommendation_user)