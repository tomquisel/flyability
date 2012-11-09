# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forecast'
        db.create_table(u'weather_forecast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteviewer.Site'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('fetch_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'weather', ['Forecast'])

        # Adding model 'ForecastValue'
        db.create_table(u'weather_forecastvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forecast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Forecast'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'weather', ['ForecastValue'])

        # Adding model 'Observation'
        db.create_table(u'weather_observation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['siteviewer.Site'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('fetch_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'weather', ['Observation'])

        # Adding model 'ObservationValue'
        db.create_table(u'weather_observationvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weather.Observation'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'weather', ['ObservationValue'])


    def backwards(self, orm):
        # Deleting model 'Forecast'
        db.delete_table(u'weather_forecast')

        # Deleting model 'ForecastValue'
        db.delete_table(u'weather_forecastvalue')

        # Deleting model 'Observation'
        db.delete_table(u'weather_observation')

        # Deleting model 'ObservationValue'
        db.delete_table(u'weather_observationvalue')


    models = {
        u'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'continent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'weather.observationvalue': {
            'Meta': {'object_name': 'ObservationValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.Observation']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['weather']