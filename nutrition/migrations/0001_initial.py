# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FoodGroup'
        db.create_table('nutrition_foodgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('nutrition', ['FoodGroup'])

        # Adding model 'Food'
        db.create_table('nutrition_food', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ndb_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('food_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='foods', to=orm['nutrition.FoodGroup'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('other_names', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('fndds_profile', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('inedible_parts_description', self.gf('django.db.models.fields.CharField')(max_length=135, null=True, blank=True)),
            ('inedible_parts_percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('nitrogen_to_protein_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('protein_to_calories_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('fat_to_calories_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('carb_to_calories_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('nutrition', ['Food'])

        # Adding model 'Nutrient'
        db.create_table('nutrition_nutrient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('tagname', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('value_decimal_places', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('sr_order', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal('nutrition', ['Nutrient'])

        # Adding model 'Source'
        db.create_table('nutrition_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('nutrition', ['Source'])

        # Adding model 'Derivation'
        db.create_table('nutrition_derivation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('nutrition', ['Derivation'])

        # Adding model 'DataSource'
        db.create_table('nutrition_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datasrc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=135, null=True, blank=True)),
            ('vol_city', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('issue_state', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('start_page', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('end_page', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('nutrition', ['DataSource'])

        # Adding model 'NutrientValue'
        db.create_table('nutrition_nutrientvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nutrient_values', to=orm['nutrition.Food'])),
            ('nutrient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutrition.Nutrient'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('data_points', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('standard_error', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutrition.Source'])),
            ('derivation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutrition.Derivation'], null=True, blank=True)),
            ('inferred_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='influenced_nutrient_values', null=True, to=orm['nutrition.Food'])),
            ('added', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('studies', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('degrees_of_freedom', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('lower_error_bound', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('upper_error_bound', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('statistical_comments', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('confidence_code', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('nutrition', ['NutrientValue'])

        # Adding unique constraint on 'NutrientValue', fields ['food', 'nutrient']
        db.create_unique('nutrition_nutrientvalue', ['food_id', 'nutrient_id'])

        # Adding M2M table for field data_sources on 'NutrientValue'
        db.create_table('nutrition_nutrientvalue_data_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nutrientvalue', models.ForeignKey(orm['nutrition.nutrientvalue'], null=False)),
            ('datasource', models.ForeignKey(orm['nutrition.datasource'], null=False))
        ))
        db.create_unique('nutrition_nutrientvalue_data_sources', ['nutrientvalue_id', 'datasource_id'])

        # Adding model 'Weight'
        db.create_table('nutrition_weight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weights', to=orm['nutrition.Food'])),
            ('sequence_number', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('grams', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=1)),
            ('data_points', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('standard_deviation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('nutrition', ['Weight'])

        # Adding unique constraint on 'Weight', fields ['food', 'sequence_number']
        db.create_unique('nutrition_weight', ['food_id', 'sequence_number'])

        # Adding model 'Footnote'
        db.create_table('nutrition_footnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(related_name='footnotes', to=orm['nutrition.Food'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('footnote_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('nutrient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nutrition.Nutrient'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('nutrition', ['Footnote'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Weight', fields ['food', 'sequence_number']
        db.delete_unique('nutrition_weight', ['food_id', 'sequence_number'])

        # Removing unique constraint on 'NutrientValue', fields ['food', 'nutrient']
        db.delete_unique('nutrition_nutrientvalue', ['food_id', 'nutrient_id'])

        # Deleting model 'FoodGroup'
        db.delete_table('nutrition_foodgroup')

        # Deleting model 'Food'
        db.delete_table('nutrition_food')

        # Deleting model 'Nutrient'
        db.delete_table('nutrition_nutrient')

        # Deleting model 'Source'
        db.delete_table('nutrition_source')

        # Deleting model 'Derivation'
        db.delete_table('nutrition_derivation')

        # Deleting model 'DataSource'
        db.delete_table('nutrition_datasource')

        # Deleting model 'NutrientValue'
        db.delete_table('nutrition_nutrientvalue')

        # Removing M2M table for field data_sources on 'NutrientValue'
        db.delete_table('nutrition_nutrientvalue_data_sources')

        # Deleting model 'Weight'
        db.delete_table('nutrition_weight')

        # Deleting model 'Footnote'
        db.delete_table('nutrition_footnote')


    models = {
        'nutrition.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'datasrc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'end_page': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_state': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '135', 'null': 'True', 'blank': 'True'}),
            'start_page': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vol_city': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'nutrition.derivation': {
            'Meta': {'object_name': 'Derivation'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'nutrition.food': {
            'Meta': {'object_name': 'Food'},
            'carb_to_calories_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fat_to_calories_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'fndds_profile': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'food_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'foods'", 'to': "orm['nutrition.FoodGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inedible_parts_description': ('django.db.models.fields.CharField', [], {'max_length': '135', 'null': 'True', 'blank': 'True'}),
            'inedible_parts_percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'ndb_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'nitrogen_to_protein_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'other_names': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'protein_to_calories_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'nutrition.foodgroup': {
            'Meta': {'object_name': 'FoodGroup'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'nutrition.footnote': {
            'Meta': {'object_name': 'Footnote'},
            'food': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'footnotes'", 'to': "orm['nutrition.Food']"}),
            'footnote_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'nutrient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Nutrient']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'nutrition.nutrient': {
            'Meta': {'object_name': 'Nutrient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'sr_order': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'tagname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'value_decimal_places': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        'nutrition.nutrientvalue': {
            'Meta': {'unique_together': "(('food', 'nutrient'),)", 'object_name': 'NutrientValue'},
            'added': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'confidence_code': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'data_points': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'data_sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'nutrient_values'", 'symmetrical': 'False', 'to': "orm['nutrition.DataSource']"}),
            'degrees_of_freedom': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'derivation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Derivation']", 'null': 'True', 'blank': 'True'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nutrient_values'", 'to': "orm['nutrition.Food']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inferred_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'influenced_nutrient_values'", 'null': 'True', 'to': "orm['nutrition.Food']"}),
            'lower_error_bound': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'maximum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'minimum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'nutrient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Nutrient']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutrition.Source']"}),
            'standard_error': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'statistical_comments': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'studies': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'upper_error_bound': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'})
        },
        'nutrition.source': {
            'Meta': {'object_name': 'Source'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'nutrition.weight': {
            'Meta': {'unique_together': "(('food', 'sequence_number'),)", 'object_name': 'Weight'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            'data_points': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weights'", 'to': "orm['nutrition.Food']"}),
            'grams': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence_number': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'standard_deviation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '3', 'blank': 'True'})
        }
    }

    complete_apps = ['nutrition']
