# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('recipes_tag')

        # Adding model 'UserRecipeRating'
        db.create_table('recipes_userreciperating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Recipe'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('recipes', ['UserRecipeRating'])

        # Adding model 'UserIngredientRating'
        db.create_table('recipes_useringredientrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Ingredient'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('recipes', ['UserIngredientRating'])

        # Adding model 'KitchenTool'
        db.create_table('recipes_kitchentool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('recipes', ['KitchenTool'])

        # Adding M2M table for field user on 'KitchenTool'
        db.create_table('recipes_kitchentool_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kitchentool', models.ForeignKey(orm['recipes.kitchentool'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('recipes_kitchentool_user', ['kitchentool_id', 'user_id'])

        # Adding model 'PantryItem'
        db.create_table('recipes_pantryitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Ingredient'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.MeasurementUnit'], null=True, blank=True)),
        ))
        db.send_create_signal('recipes', ['PantryItem'])

        # Adding model 'RecipeKitchenTool'
        db.create_table('recipes_recipekitchentool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tools', to=orm['recipes.Recipe'])),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.KitchenTool'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1, null=True, blank=True)),
        ))
        db.send_create_signal('recipes', ['RecipeKitchenTool'])

        # Adding field 'RecipeIngredient.max_quantity'
        db.add_column('recipes_recipeingredient', 'max_quantity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Deleting field 'MeasurementUnit.weight'
        db.delete_column('recipes_measurementunit', 'weight')

        # Adding M2M table for field equivalent_units on 'MeasurementUnit'
        db.create_table('recipes_measurementunit_equivalent_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_measurementunit', models.ForeignKey(orm['recipes.measurementunit'], null=False)),
            ('to_measurementunit', models.ForeignKey(orm['recipes.measurementunit'], null=False))
        ))
        db.create_unique('recipes_measurementunit_equivalent_units', ['from_measurementunit_id', 'to_measurementunit_id'])

        # Adding field 'Recipe.average_rating'
        db.add_column('recipes_recipe', 'average_rating', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Recipe.notes'
        db.add_column('recipes_recipe', 'notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Recipe.tags'
        db.add_column('recipes_recipe', 'tags', self.gf('tagging.fields.TagField')(default=''), keep_default=False)

        # Removing M2M table for field tags on 'Recipe'
        db.delete_table('recipes_recipe_tags')

        # Adding field 'Ingredient.average_rating'
        db.add_column('recipes_ingredient', 'average_rating', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding M2M table for field equivalent_ingredients on 'Ingredient'
        db.create_table('recipes_ingredient_equivalent_ingredients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_ingredient', models.ForeignKey(orm['recipes.ingredient'], null=False)),
            ('to_ingredient', models.ForeignKey(orm['recipes.ingredient'], null=False))
        ))
        db.create_unique('recipes_ingredient_equivalent_ingredients', ['from_ingredient_id', 'to_ingredient_id'])


    def backwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('recipes_tag', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('recipes', ['Tag'])

        # Deleting model 'UserRecipeRating'
        db.delete_table('recipes_userreciperating')

        # Deleting model 'UserIngredientRating'
        db.delete_table('recipes_useringredientrating')

        # Deleting model 'KitchenTool'
        db.delete_table('recipes_kitchentool')

        # Removing M2M table for field user on 'KitchenTool'
        db.delete_table('recipes_kitchentool_user')

        # Deleting model 'PantryItem'
        db.delete_table('recipes_pantryitem')

        # Deleting model 'RecipeKitchenTool'
        db.delete_table('recipes_recipekitchentool')

        # Deleting field 'RecipeIngredient.max_quantity'
        db.delete_column('recipes_recipeingredient', 'max_quantity')

        # Adding field 'MeasurementUnit.weight'
        db.add_column('recipes_measurementunit', 'weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Removing M2M table for field equivalent_units on 'MeasurementUnit'
        db.delete_table('recipes_measurementunit_equivalent_units')

        # Deleting field 'Recipe.average_rating'
        db.delete_column('recipes_recipe', 'average_rating')

        # Deleting field 'Recipe.notes'
        db.delete_column('recipes_recipe', 'notes')

        # Deleting field 'Recipe.tags'
        db.delete_column('recipes_recipe', 'tags')

        # Adding M2M table for field tags on 'Recipe'
        db.create_table('recipes_recipe_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm['recipes.recipe'], null=False)),
            ('tag', models.ForeignKey(orm['recipes.tag'], null=False))
        ))
        db.create_unique('recipes_recipe_tags', ['recipe_id', 'tag_id'])

        # Deleting field 'Ingredient.average_rating'
        db.delete_column('recipes_ingredient', 'average_rating')

        # Removing M2M table for field equivalent_ingredients on 'Ingredient'
        db.delete_table('recipes_ingredient_equivalent_ingredients')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'recipes.ingredient': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ingredient'},
            'average_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'equivalent_ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'equivalent_ingredients_rel_+'", 'to': "orm['recipes.Ingredient']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'recipes.junkrecipe': {
            'Meta': {'object_name': 'JunkRecipe'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_added': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'recipes.kitchentool': {
            'Meta': {'object_name': 'KitchenTool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'recipes.measurementunit': {
            'Meta': {'object_name': 'MeasurementUnit'},
            'equivalent_units': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'equivalent_units_rel_+'", 'to': "orm['recipes.MeasurementUnit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'recipes.pantryitem': {
            'Meta': {'object_name': 'PantryItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Ingredient']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.MeasurementUnit']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'recipes.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'recipes.recipe': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Recipe'},
            'average_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'cook_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'creates_ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Ingredient']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'directions': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_photos': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'main_photos'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['recipes.Photo']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['recipes.Photo']", 'null': 'True', 'blank': 'True'}),
            'prep_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'servings': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'recipes.recipeingredient': {
            'Meta': {'object_name': 'RecipeIngredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Ingredient']"}),
            'max_quantity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'optional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preparation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'to': "orm['recipes.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.MeasurementUnit']", 'null': 'True', 'blank': 'True'})
        },
        'recipes.recipekitchentool': {
            'Meta': {'object_name': 'RecipeKitchenTool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tools'", 'to': "orm['recipes.Recipe']"}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.KitchenTool']"})
        },
        'recipes.useringredientrating': {
            'Meta': {'object_name': 'UserIngredientRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Ingredient']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'recipes.userreciperating': {
            'Meta': {'object_name': 'UserRecipeRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['recipes']
