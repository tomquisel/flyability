# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Site.takeoffDirLeft'
        db.delete_column('siteviewer_site', 'takeoffDirLeft')

        # Deleting field 'Site.takeoffDirRight'
        db.delete_column('siteviewer_site', 'takeoffDirRight')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Site.takeoffDirLeft'
        raise RuntimeError("Cannot reverse this migration. 'Site.takeoffDirLeft' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.takeoffDirRight'
        raise RuntimeError("Cannot reverse this migration. 'Site.takeoffDirRight' and its values cannot be restored.")

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
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['siteviewer']