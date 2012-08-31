# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.state'
        db.add_column('siteviewer_site', 'state',
                      self.gf('django.db.models.fields.CharField')(default='New York', max_length=255),
                      keep_default=False)

        # Adding field 'Site.country'
        db.add_column('siteviewer_site', 'country',
                      self.gf('django.db.models.fields.CharField')(default='United States', max_length=255),
                      keep_default=False)

        # Adding field 'Site.continent'
        db.add_column('siteviewer_site', 'continent',
                      self.gf('django.db.models.fields.CharField')(default='North America', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.state'
        db.delete_column('siteviewer_site', 'state')

        # Deleting field 'Site.country'
        db.delete_column('siteviewer_site', 'country')

        # Deleting field 'Site.continent'
        db.delete_column('siteviewer_site', 'continent')


    models = {
        'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'takeoffDirLeft': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'takeoffDirRight': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['siteviewer']