# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.website'
        db.add_column('siteviewer_site', 'website',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Site.pgearthSite'
        db.add_column('siteviewer_site', 'pgearthSite',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.website'
        db.delete_column('siteviewer_site', 'website')

        # Deleting field 'Site.pgearthSite'
        db.delete_column('siteviewer_site', 'pgearthSite')


    models = {
        'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'continent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'pgearthSite': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'takeoffDirLeft': ('django.db.models.fields.IntegerField', [], {}),
            'takeoffDirRight': ('django.db.models.fields.IntegerField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['siteviewer']