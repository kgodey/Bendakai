from models import Recipe, Ingredient, JunkRecipe, RecipeIngredient, Tag, Photo, MeasurementUnit
from forms import RecipeForm, RecipeIngredientsFormset
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required

def all_recipes(request):
	try:
		recipes = Recipe.objects.filter(is_public=True)
	except Recipe.DoesNotExist:
		raise Http404
#	paginator = Paginator(recipes, 5)
#	try:
#		page = int(request.GET.get('page', '1'))
#	except ValueError:
#		page = 1
#	try:
#		recipes = paginator.page(page)
#	except (EmptyPage, InvalidPage):
#		recipes = paginator.page(paginator.num_pages)
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
	else:
		form = RecipeForm()
		formset = RecipeIngredientsFormset()
	return render_to_response('recipes/add_recipe.html', {'form': form, 'formset': formset}, context_instance=RequestContext(request))


def correct_recipe(request):
	if request.method == 'POST':
		junk = JunkRecipe.objects.get(id=request.POST['junk_id'])
		form = RecipeForm(request.POST, request.FILES)
		if form.is_valid():
			recipe = form.save()
			junk.is_added = True
			junk.save()
			formset = RecipeIngredientsFormset(request.POST, request.FILES, instance=recipe)
			if formset.is_valid():
				formset.save()
	else:
		junk = JunkRecipe.objects.filter(is_added=False).order_by('?')[0]
		form = RecipeForm()
		formset = RecipeIngredientsFormset()
	return render_to_response('recipes/correct_recipe.html', {'form': form, 'formset': formset, 'junk': junk}, context_instance=RequestContext(request))


def view_recipe(request, id):
	recipe = get_object_or_404(Recipe, id=id)
	return render_to_response('recipes/view_recipe.html', {'recipe': recipe,}, context_instance=RequestContext(request))


def edit_recipe(request, id):
	recipe = get_object_or_404(Recipe, id=id)
	if request.method == 'POST':
		form = RecipeForm(request.POST, request.FILES, instance=recipe)
		formset = RecipeIngredientsFormset(request.POST, request.FILES, instance=recipe)
		if form.is_valid():
			recipe = form.save(commit=False)
			if formset.is_valid():
				formset.save()
				recipe.save()
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


def userpage(request, username):
	if request.user.username == username:
		recipes = Recipe.objects.filter(user__username = username)
		return render_to_response('recipes/userpage.html', {'recipes': recipes,}, context_instance=RequestContext(request))
	else:
		return render_to_response('recipes/forbidden.html', context_instance=RequestContext(request))