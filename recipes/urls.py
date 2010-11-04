from django.conf.urls.defaults import *
import views
from django.shortcuts import render_to_response

urlpatterns = patterns('',
	url(r'^$', views.homepage, name='homepage'),
	url(r'^all/$', views.all_recipes, name='all_recipes'),
	url(r'^add/$', views.add_recipe, name='add_recipe'),
	url(r'^ajax/ingredient/$', views.ingredient_ajax, name='ingredient_ajax'),
	url(r'^ajax/unit/$', views.unit_ajax, name='unit_ajax'),
	url(r'^correct/$', views.correct_recipe, name='correct_recipe'),
	url(r'^junk/$', views.all_junk_recipes, name='all_junk_recipes'),
	url(r'^edit/(?P<id>\d+)/$', views.edit_recipe, name='edit_recipe'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^people/(?P<username>\w+)/$', views.userpage, name='userpage'),
	url(r'^(?P<id>\d+)/$', views.view_recipe, name='view_recipe'),
)
