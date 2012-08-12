# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table('siteviewer_site', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('takeoffDirLeft', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('takeoffDirRight', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('siteviewer', ['Site'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table('siteviewer_site')


    models = {
        'siteviewer.site': {
            'Meta': {'object_name': 'Site'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'takeoffDirLeft': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'takeoffDirRight': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['siteviewer']