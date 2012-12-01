# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForecastData'
        db.create_table(u'weather_forecastdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forecast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Forecast'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weather', ['ForecastData'])

        # Adding model 'ObservationData'
        db.create_table(u'weather_observationdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Observation'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weather', ['ObservationData'])


    def backwards(self, orm):
        # Deleting model 'ForecastData'
        db.delete_table(u'weather_forecastdata')

        # Deleting model 'ObservationData'
        db.delete_table(u'weather_observationdata')


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
        u'weather.forecastvalue': {
            'Meta': {'object_name': 'ForecastValue'},
            'forecast': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.Forecast']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
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
        u'weather.observationvalue': {
            'Meta': {'object_name': 'ObservationValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.Observation']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['weather']