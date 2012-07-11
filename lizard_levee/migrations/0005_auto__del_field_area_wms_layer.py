# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Area.wms_layer'
        db.delete_column('lizard_levee_area', 'wms_layer_id')

        # Adding M2M table for field wms_layer on 'Area'
        db.create_table('lizard_levee_area_wms_layer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('area', models.ForeignKey(orm['lizard_levee.area'], null=False)),
            ('wmssource', models.ForeignKey(orm['lizard_wms.wmssource'], null=False))
        ))
        db.create_unique('lizard_levee_area_wms_layer', ['area_id', 'wmssource_id'])


    def backwards(self, orm):
        
        # Adding field 'Area.wms_layer'
        db.add_column('lizard_levee_area', 'wms_layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_wms.WMSSource'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field wms_layer on 'Area'
        db.delete_table('lizard_levee_area_wms_layer')


    models = {
        'lizard_levee.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'wms_layer': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_wms.WMSSource']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.informationpointer': {
            'Meta': {'object_name': 'InformationPointer'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'information_pointers'", 'null': 'True', 'to': "orm['lizard_levee.Area']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'more_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_maptree.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_maptree.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'})
        },
        'lizard_wms.wmsconnection': {
            'Meta': {'object_name': 'WMSConnection'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_maptree.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.TextField', [], {'default': '\'{"buffer": 0, "reproject": true, "isBaseLayer": false, "opacity": 0.5}\''}),
            'params': ('django.db.models.fields.TextField', [], {'default': '\'{"height": "256", "width": "256", "layers": "%s", "styles": "", "format": "image/png", "tiled": "true", "transparent": "true"}\''}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.3.0'", 'max_length': '20'}),
            'xml': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'lizard_wms.wmssource': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WMSSource'},
            'bbox': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_maptree.Category']", 'null': 'True', 'blank': 'True'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_wms.WMSConnection']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend_url': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lizard_levee']
