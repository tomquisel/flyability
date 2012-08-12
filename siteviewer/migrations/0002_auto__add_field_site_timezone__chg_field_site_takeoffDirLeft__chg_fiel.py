# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.timezone'
        db.add_column('siteviewer_site', 'timezone',
                      self.gf('django.db.models.fields.CharField')(default='US/Eastern', max_length=255),
                      keep_default=False)


        # Changing field 'Site.takeoffDirLeft'
        db.alter_column('siteviewer_site', 'takeoffDirLeft', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Site.name'
        db.alter_column('siteviewer_site', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True))

        # Changing field 'Site.takeoffDirRight'
        db.alter_column('siteviewer_site', 'takeoffDirRight', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'Site.timezone'
        db.delete_column('siteviewer_site', 'timezone')


        # Changing field 'Site.takeoffDirLeft'
        db.alter_column('siteviewer_site', 'takeoffDirLeft', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Site.name'
        db.alter_column('siteviewer_site', 'name', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True))

        # Changing field 'Site.takeoffDirRight'
        db.alter_column('siteviewer_site', 'takeoffDirRight', self.gf('django.db.models.fields.CharField')(max_length=20))

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
        }
    }

    complete_apps = ['siteviewer']