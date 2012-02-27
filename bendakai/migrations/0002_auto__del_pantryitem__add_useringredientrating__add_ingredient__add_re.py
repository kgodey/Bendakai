# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'PantryItem'
        db.delete_table('bendakai_pantryitem')

        # Removing M2M table for field users on 'PantryItem'
        db.delete_table('bendakai_pantryitem_users')

        # Adding model 'UserIngredientRating'
        db.create_table('bendakai_useringredientrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['bendakai.Ingredient'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bendakai', ['UserIngredientRating'])

        # Adding model 'Ingredient'
        db.create_table('bendakai_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('bendakai', ['Ingredient'])

        # Adding M2M table for field equivalent_ingredients on 'Ingredient'
        db.create_table('bendakai_ingredient_equivalent_ingredients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_ingredient', models.ForeignKey(orm['bendakai.ingredient'], null=False)),
            ('to_ingredient', models.ForeignKey(orm['bendakai.ingredient'], null=False))
        ))
        db.create_unique('bendakai_ingredient_equivalent_ingredients', ['from_ingredient_id', 'to_ingredient_id'])

        # Adding M2M table for field pantry_users on 'Ingredient'
        db.create_table('bendakai_ingredient_pantry_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ingredient', models.ForeignKey(orm['bendakai.ingredient'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('bendakai_ingredient_pantry_users', ['ingredient_id', 'user_id'])

        # Adding model 'RecipeIngredient'
        db.create_table('bendakai_recipeingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ingredients', to=orm['bendakai.Recipe'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipes', to=orm['bendakai.Ingredient'])),
            ('min_quantity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('max_quantity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bendakai.MeasurementUnit'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('optional', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bendakai', ['RecipeIngredient'])

        # Adding model 'MeasurementUnit'
        db.create_table('bendakai_measurementunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('bendakai', ['MeasurementUnit'])

        # Adding M2M table for field equivalent_units on 'MeasurementUnit'
        db.create_table('bendakai_measurementunit_equivalent_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_measurementunit', models.ForeignKey(orm['bendakai.measurementunit'], null=False)),
            ('to_measurementunit', models.ForeignKey(orm['bendakai.measurementunit'], null=False))
        ))
        db.create_unique('bendakai_measurementunit_equivalent_units', ['from_measurementunit_id', 'to_measurementunit_id'])

        # Deleting field 'Recipe.ingredients'
        db.delete_column('bendakai_recipe', 'ingredients')


    def backwards(self, orm):
        
        # Adding model 'PantryItem'
        db.create_table('bendakai_pantryitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('bendakai', ['PantryItem'])

        # Adding M2M table for field users on 'PantryItem'
        db.create_table('bendakai_pantryitem_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pantryitem', models.ForeignKey(orm['bendakai.pantryitem'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('bendakai_pantryitem_users', ['pantryitem_id', 'user_id'])

        # Deleting model 'UserIngredientRating'
        db.delete_table('bendakai_useringredientrating')

        # Deleting model 'Ingredient'
        db.delete_table('bendakai_ingredient')

        # Removing M2M table for field equivalent_ingredients on 'Ingredient'
        db.delete_table('bendakai_ingredient_equivalent_ingredients')

        # Removing M2M table for field pantry_users on 'Ingredient'
        db.delete_table('bendakai_ingredient_pantry_users')

        # Deleting model 'RecipeIngredient'
        db.delete_table('bendakai_recipeingredient')

        # Deleting model 'MeasurementUnit'
        db.delete_table('bendakai_measurementunit')

        # Removing M2M table for field equivalent_units on 'MeasurementUnit'
        db.delete_table('bendakai_measurementunit_equivalent_units')

        # User chose to not deal with backwards NULL issues for 'Recipe.ingredients'
        raise RuntimeError("Cannot reverse this migration. 'Recipe.ingredients' and its values cannot be restored.")


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
        'bendakai.ingredient': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ingredient'},
            'equivalent_ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'equivalent_ingredients_rel_+'", 'null': 'True', 'to': "orm['bendakai.Ingredient']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pantry_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pantry_items'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'bendakai.measurementunit': {
            'Meta': {'object_name': 'MeasurementUnit'},
            'equivalent_units': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'equivalent_units_rel_+'", 'null': 'True', 'to': "orm['bendakai.MeasurementUnit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'bendakai.recipe': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Recipe'},
            'cook_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'prep_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'servings': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'starred_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'starred_recipe_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bendakai.recipeingredient': {
            'Meta': {'object_name': 'RecipeIngredient'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes'", 'to': "orm['bendakai.Ingredient']"}),
            'max_quantity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_quantity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'optional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'to': "orm['bendakai.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bendakai.MeasurementUnit']", 'null': 'True', 'blank': 'True'})
        },
        'bendakai.useringredientrating': {
            'Meta': {'object_name': 'UserIngredientRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['bendakai.Ingredient']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'bendakai.userreciperating': {
            'Meta': {'object_name': 'UserRecipeRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['bendakai.Recipe']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['bendakai']
