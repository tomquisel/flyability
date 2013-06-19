# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeatherSummary'
        db.create_table(u'weather_weathersummary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteviewer.Site'])),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weather', ['WeatherSummary'])


    def backwards(self, orm):
        # Adding model 'ForecastValue'
        db.create_table(u'weather_forecastvalue', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('forecast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Forecast'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        # Deleting model 'WeatherSummary'
        db.delete_table(u'weather_weathersummary')


    models = {
        u'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'continent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pgearthSite': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'takeoffObj': ('django.db.models.fields.TextField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'weather.forecast': {
            'Meta': {'object_name': 'Forecast'},
            'fetch_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteviewer.Site']"})
        },
        u'weather.forecastdata': {
            'Meta': {'object_name': 'ForecastData'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'forecast': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.Forecast']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'weather.observation': {
            'Meta': {'object_name': 'Observation'},
            'fetch_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteviewer.Site']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'weather.observationdata': {
            'Meta': {'object_name': 'ObservationData'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.Observation']"})
        },
        u'weather.weathersummary': {
            'Meta': {'object_name': 'WeatherSummary'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['siteviewer.Site']"})
        }
    }

    complete_apps = ['weather']
