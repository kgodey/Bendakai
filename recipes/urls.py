from django.conf.urls.defaults import *
import views
from django.shortcuts import render_to_response

urlpatterns = patterns('',
	url(r'^$', views.all_recipes, name='all_recipes'),
	url(r'^add/$', views.add_recipe, name='add_recipe'),
	url(r'^correct/$', views.correct_recipe, name='correct_recipe'),
	url(r'^junk/$', views.all_junk_recipes, name='all_junk_recipes'),
	url(r'^edit/(?P<id>\d+)/$', views.edit_recipe, name='edit_recipe'),
	url(r'^(?P<id>\d+)/$', views.view_recipe, name='view_recipe'),
)
