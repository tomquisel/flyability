# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Forecast', fields ['fetchTime']
        db.create_index('weather_forecast', ['fetchTime'])


    def backwards(self, orm):
        # Removing index on 'Forecast', fields ['fetchTime']
        db.delete_index('weather_forecast', ['fetchTime'])


    models = {
        'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'takeoffDirLeft': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'takeoffDirRight': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'weather.forecast': {
            'Meta': {'object_name': 'Forecast'},
            'fetchTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['siteviewer.Site']"})
        },
        'weather.forecastvalue': {
            'Meta': {'object_name': 'ForecastValue'},
            'forecast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weather.Forecast']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'weather.observation': {
            'Meta': {'object_name': 'Observation'},
            'fetchTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['siteviewer.Site']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'weather.observationvalue': {
            'Meta': {'object_name': 'ObservationValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weather.Observation']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['weather']