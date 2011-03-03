from django.conf.urls.defaults import *
import views
from django.shortcuts import render_to_response

urlpatterns = patterns('',
	url(r'^$', views.homepage, name='homepage'),
	url(r'^recent/$', views.all_recipes, name='all_recipes'),
	url(r'^add/$', views.add_recipe, name='add_recipe'),
	url(r'^ajax/ingredient/$', views.ingredient_ajax, name='ingredient_ajax'),
	url(r'^ajax/unit/$', views.unit_ajax, name='unit_ajax'),
	url(r'^ajax/tag/$', views.tag_ajax, name='tag_ajax'),
	url(r'^correct/$', views.correct_recipe, name='correct_recipe'),
	url(r'^edit/(?P<id>\d+)/$', views.edit_recipe, name='edit_recipe'),
	url(r'^plaintext/(?P<junk_id>\d+)/$', views.junk_popout, name='junk_popout'),
	url(r'^search/$', views.simple_search, name='simple_search'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^people/(?P<username>\w+)/$', views.userpage, name='userpage'),
	url(r'^tags/(?P<tag>[-\w ]+)/$', views.recipe_by_tag, name='recipe_by_tag'),
	url(r'^ingredients/(?P<ingredient>[-\w\W ]+)/$', views.recipe_by_ingredient, name='recipe_by_ingredient'),
	url(r'^rate_ingredients/$', views.ingredient_list, name='ingredient_list'),
	url(r'^(?P<id>\d+)/$', views.view_recipe, name='view_recipe'),
	url(r'^ajax/get_user_recipe_rating/(?P<recipe_id>\d+)/$', views.get_user_recipe_rating, name='get_user_recipe_rating'),
	url(r'^ajax/save_user_recipe_rating/(?P<recipe_id>\d+)/$', views.save_user_recipe_rating, name='save_user_recipe_rating'),
	url(r'^ajax/get_user_ingredient_rating/(?P<ingredient_id>\d+)/$', views.get_user_ingredient_rating, name='get_user_ingredient_rating'),
	url(r'^ajax/save_user_ingredient_rating/(?P<ingredient_id>\d+)/$', views.save_user_ingredient_rating, name='save_user_ingredient_rating'),
)
