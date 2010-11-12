from recipes.models import Recipe

def search_for(term):
	by_ingredient = Recipe.objects.filter(ingredients__ingredient__name__icontains = search_term)
	by_directions = Recipe.objects.filter(directions__icontains = search_term)
	return QuerySetChain(by_ingredient, by_directions)