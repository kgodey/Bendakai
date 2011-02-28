from models import Recipe, Ingredient, JunkRecipe, RecipeIngredient, Photo, MeasurementUnit, UserRecipeRating, UserIngredientRating
from forms import RecipeForm, RecipeIngredientsFormset
from tagging.models import Tag, TaggedItem
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q, Count
import random
from django.views.decorators.csrf import csrf_exempt

def all_recipes(request):
	try:
		recipes = Recipe.objects.filter(is_public=True)
	except Recipe.DoesNotExist:
		raise Http404
	paginator = Paginator(recipes, 5)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		recipes = paginator.page(page)
	except (EmptyPage, InvalidPage):
		recipes = paginator.page(paginator.num_pages)
	return render_to_response('recipes/allrecipes.html', {'recipes': recipes,}, context_instance=RequestContext(request))

@login_required
def add_recipe(request):
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			recipe = form.save(commit=False)
			recipe.user = request.user
			recipe.save()
			formset = RecipeIngredientsFormset(request.POST, request.FILES, instance=recipe)
			if formset.is_valid():
				formset.save()
				recipe.save()
				return render_to_response('recipes/view_recipe.html', {'recipe': recipe,}, context_instance=RequestContext(request))
			else:
				recipe.delete()
		else:
			formset = RecipeIngredientsFormset(request.POST, request.FILES)
	else:
		form = RecipeForm()
		formset = RecipeIngredientsFormset()
	return render_to_response('recipes/add_recipe.html', {'form': form, 'formset': formset}, context_instance=RequestContext(request))

@login_required
def correct_recipe(request):
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			recipe = form.save(commit=False)
			recipe.user = request.user
			recipe.save()
			junk_id = request.POST['junkid']
			junk = JunkRecipe.objects.get(id = junk_id)
			formset = RecipeIngredientsFormset(request.POST, request.FILES, instance=recipe)
			if formset.is_valid():
				formset.save()
				recipe.save()
				junk.is_added = True
				junk.derived_recipe = recipe
				junk.save()
				return render_to_response('recipes/view_recipe.html', {'recipe': recipe,}, context_instance=RequestContext(request))
			else:
				recipe.delete()
		else:
			junk_id = request.POST['junkid']
			junk = JunkRecipe.objects.get(id = junk_id)
			formset = RecipeIngredientsFormset(request.POST, request.FILES)
	else:
		junk = random.choice(JunkRecipe.objects.filter(is_added = False))
		form = RecipeForm()
		formset = RecipeIngredientsFormset()
	return render_to_response('recipes/correct_recipe.html', {'form': form, 'formset': formset, 'junk': junk}, context_instance=RequestContext(request))


def view_recipe(request, id):
	recipe = get_object_or_404(Recipe, id=id)
	return render_to_response('recipes/view_recipe.html', {'recipe': recipe,}, context_instance=RequestContext(request))

@login_required
def edit_recipe(request, id):
	recipe = get_object_or_404(Recipe, id=id)
	if not recipe.user == request.user:
		return render_to_response('recipes/forbidden.html', context_instance=RequestContext(request))
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES, instance=recipe)
		formset = RecipeIngredientsFormset(request.POST, request.FILES, instance=recipe)
		if form.is_valid():
			recipe = form.save(commit=False)
			if formset.is_valid():
				formset.save()
				recipe.save()
				return render_to_response('recipes/view_recipe.html', {'recipe': recipe,}, context_instance=RequestContext(request))
	else:
		form = RecipeForm(instance=recipe)
		formset = RecipeIngredientsFormset(instance=recipe)
	return render_to_response('recipes/edit_recipe.html', {'recipe': recipe, 'form': form, 'formset': formset}, context_instance=RequestContext(request))


def all_junk_recipes(request):
	try:
		junk_recipes = JunkRecipe.objects.all()
	except JunkRecipe.DoesNotExist:
		raise Http404
#	paginator = Paginator(junk_recipes, 10)
#	try:
#		page = int(request.GET.get('page', '1'))
#	except ValueError:
#		page = 1
#	try:
#		junk_recipes = paginator.page(page)
#	except (EmptyPage, InvalidPage):
#		junk_recipes = paginator.page(paginator.num_pages)
	return render_to_response('recipes/allrecipes.html', {'junk_recipes': junk_recipes,}, context_instance=RequestContext(request))


def ingredient_ajax(request):
	if request.method == 'GET':
		if 'term' in request.GET:
			query = request.GET['term']
			ingredients = Ingredient.objects.filter(name__icontains=query).order_by('name')
			responselist = []
			for i in ingredients:
				responselist.append(i.name)
			response = json.dumps(responselist)
			return HttpResponse(response, mimetype='application/json')
		else:
			return HttpResponse('[]', mimetype='application/json')


def unit_ajax(request):
	if request.method == 'GET':
		if 'term' in request.GET:
			query = request.GET['term']
			units = MeasurementUnit.objects.filter(name__icontains=query).order_by('name')
			responselist = []
			for u in units:
				responselist.append(u.name)
			response = json.dumps(responselist)
			return HttpResponse(response, mimetype='application/json')
		else:
			return HttpResponse('[]', mimetype='application/json')


def login(request):
	return render_to_response('recipes/login.html', context_instance=RequestContext(request))


def logout_view(request):
	logout(request)
	return render_to_response('recipes/loggedout.html', context_instance=RequestContext(request))

def userpage(request, username):
	recipe_user = User.objects.get(username = username)
	if request.user.username == username:
		try:
			recipes = Recipe.objects.filter(user__username = username)
		except Recipe.DoesNotExist:
			raise Http404
		paginator = Paginator(recipes, 5)
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1
		try:
			recipes = paginator.page(page)
		except (EmptyPage, InvalidPage):
			recipes = paginator.page(paginator.num_pages)
		return render_to_response('recipes/userpage.html', {'recipes': recipes, 'recipe_user': recipe_user}, context_instance=RequestContext(request))
	else:
		try:
			recipes = Recipe.objects.filter(user__username = username, is_public=True)
		except Recipe.DoesNotExist:
			raise Http404
		paginator = Paginator(recipes, 5)
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1
		try:
			recipes = paginator.page(page)
		except (EmptyPage, InvalidPage):
			recipes = paginator.page(paginator.num_pages)
		return render_to_response('recipes/userpage.html', {'recipes': recipes, 'recipe_user': recipe_user}, context_instance=RequestContext(request))

def homepage(request):
	return render_to_response('recipes/index.html', context_instance=RequestContext(request))

def search(request, searchterm):
	Q_full_term = Q(ingredients__ingredient__name__icontains=searchterm) | Q(directions__icontains = searchterm) | Q(name__icontains = searchterm)
	full_term = Recipe.objects.filter(
		Q_full_term
	).distinct()
	Q_by_words = None
	for word in searchterm.split():
		if Q_by_words is None:
			Q_by_words = Q(ingredients__ingredient__name__icontains = word) | Q(directions__icontains = word) | Q(name__icontains = word)
		else:
			Q_by_words |= Q(ingredients__ingredient__name__icontains = word) | Q(directions__icontains = word) | Q(name__icontains = word)
	by_words = Recipe.objects.filter(Q_by_words).exclude(pk__in = full_term).distinct()
	return render_to_response('recipes/search.html', {'full_term': full_term, 'by_words': by_words, 'search_term': searchterm}, context_instance=RequestContext(request))

def junk_popout(request, junk_id):
	junk = JunkRecipe.objects.get(id = junk_id)
	return render_to_response('recipes/junk_popout.html', {'junk': junk,}, context_instance=RequestContext(request))

def recipe_by_tag(request, tag):
	try:
		tag_object = Tag.objects.get(name=tag)
		recipes = TaggedItem.objects.get_by_model(Recipe, tag_object)
	except Recipe.DoesNotExist:
		raise Http404
	paginator = Paginator(recipes, 5)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		recipes = paginator.page(page)
	except (EmptyPage, InvalidPage):
		recipes = paginator.page(paginator.num_pages)
	return render_to_response('recipes/recipe_by_tag.html', {'recipes': recipes, 'tag': tag_object,}, context_instance=RequestContext(request))

def recipe_by_ingredient(request, ingredient):
	recipes = Recipe.objects.filter(ingredients__ingredient__name=ingredient).distinct()
	paginator = Paginator(recipes, 5)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		recipes = paginator.page(page)
	except (EmptyPage, InvalidPage):
		recipes = paginator.page(paginator.num_pages)
	return render_to_response('recipes/recipe_by_ingredient.html', {'recipes': recipes, 'ingredient': ingredient,}, context_instance=RequestContext(request))

@login_required
def get_user_recipe_rating(request, recipe_id):
	recipe = Recipe.objects.get(id=recipe_id)
	try:
		return HttpResponse(str(recipe.ratings.get(user=request.user).rating/2.0), mimetype='text/plain')
	except UserRecipeRating.DoesNotExist:
		return HttpResponse('0', mimetype='text/plain')
	

@login_required
@csrf_exempt
def save_user_recipe_rating(request, recipe_id):
	rating = float(request.POST['score'])
	recipe = Recipe.objects.get(id=recipe_id)
	if rating == 0:
		try:
			recipe.ratings.get(user=request.user).delete()
		except:
			pass
		return HttpResponse()
	user_recipe_rating, created = recipe.ratings.get_or_create(user=request.user, defaults={'rating': rating*2,})
	if not created:
		user_recipe_rating.rating = rating*2
		user_recipe_rating.save()
	return HttpResponse()

@login_required
def get_user_ingredient_rating(request, ingredient_id):
	ingredient = Ingredient.objects.get(id=ingredient_id)
	try:
		return HttpResponse(str(ingredient.ratings.get(user=request.user).rating/2.0), mimetype='text/plain')
	except UserIngredientRating.DoesNotExist:
		return HttpResponse('0', mimetype='text/plain')


@login_required
@csrf_exempt
def save_user_ingredient_rating(request, ingredient_id):
	rating = float(request.POST['score'])
	ingredient = Ingredient.objects.get(id=ingredient_id)
	if rating == 0:
		try:
			ingredient.ratings.get(user=request.user).delete()
		except:
			pass
		return HttpResponse()
	user_ingredient_rating, created = ingredient.ratings.get_or_create(user=request.user, defaults={'rating': rating*2,})
	if not created:
		user_ingredient_rating.rating = rating*2
		user_ingredient_rating.save()
	return HttpResponse()


@login_required
def ingredient_list(request):
	ingredients = Ingredient.objects.annotate(num_recipes=Count('recipes')).order_by('-num_recipes')
	paginator = Paginator(ingredients, 20)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		ingredients = paginator.page(page)
	except (EmptyPage, InvalidPage):
		ingredients = paginator.page(paginator.num_pages)
	return render_to_response('recipes/ingredient_list.html', {'ingredients': ingredients,}, context_instance=RequestContext(request))