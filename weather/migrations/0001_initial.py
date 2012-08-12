# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forecast'
        db.create_table('weather_forecast', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteviewer.Site'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('fetchTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('weather', ['Forecast'])

        # Adding model 'ForecastValue'
        db.create_table('weather_forecastvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forecast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Forecast'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('weather', ['ForecastValue'])

        # Adding model 'Observation'
        db.create_table('weather_observation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteviewer.Site'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('fetchTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('weather', ['Observation'])

        # Adding model 'ObservationValue'
        db.create_table('weather_observationvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Observation'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('weather', ['ObservationValue'])


    def backwards(self, orm):
        # Deleting model 'Forecast'
        db.delete_table('weather_forecast')

        # Deleting model 'ForecastValue'
        db.delete_table('weather_forecastvalue')

        # Deleting model 'Observation'
        db.delete_table('weather_observation')

        # Deleting model 'ObservationValue'
        db.delete_table('weather_observationvalue')


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
            'fetchTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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