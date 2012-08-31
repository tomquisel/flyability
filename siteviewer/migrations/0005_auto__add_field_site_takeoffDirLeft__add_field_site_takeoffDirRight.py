# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.takeoffDirLeft'
        db.add_column('siteviewer_site', 'takeoffDirLeft',
                      self.gf('django.db.models.fields.IntegerField')(default=205),
                      keep_default=False)

        # Adding field 'Site.takeoffDirRight'
        db.add_column('siteviewer_site', 'takeoffDirRight',
                      self.gf('django.db.models.fields.IntegerField')(default=295),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.takeoffDirLeft'
        db.delete_column('siteviewer_site', 'takeoffDirLeft')

        # Deleting field 'Site.takeoffDirRight'
        db.delete_column('siteviewer_site', 'takeoffDirRight')


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
            'takeoffDirLeft': ('django.db.models.fields.IntegerField', [], {}),
            'takeoffDirRight': ('django.db.models.fields.IntegerField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['siteviewer']