# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ImageMap.auto_admin_value'
        db.delete_column('lizard_levee_imagemap', 'auto_admin_value')


    def backwards(self, orm):
        
        # Adding field 'ImageMap.auto_admin_value'
        db.add_column('lizard_levee_imagemap', 'auto_admin_value', self.gf('django.db.models.fields.FloatField')(default=1.0), keep_default=False)


    models = {
        'lizard_geodin.apistartingpoint': {
            'Meta': {'object_name': 'ApiStartingPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_geodin.datatype': {
            'Meta': {'object_name': 'DataType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'lizard_geodin.investigationtype': {
            'Meta': {'object_name': 'InvestigationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'lizard_geodin.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'lizard_geodin.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'data_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.DataType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigation_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.InvestigationType']"}),
            'location_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.LocationType']"}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.Project']"})
        },
        'lizard_geodin.project': {
            'Meta': {'ordering': "(u'-active', u'name')", 'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'api_starting_point': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'location_types'", 'null': 'True', 'to': "orm['lizard_geodin.ApiStartingPoint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.area': {
            'Meta': {'object_name': 'Area'},
            'cross_section_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information_pointers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.InformationPointer']", 'null': 'True', 'blank': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.Link']", 'null': 'True', 'blank': 'True'}),
            'longitudinal_cross_section_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'segments_jsonfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'wms_layers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_wms.WMSSource']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemap': {
            'Meta': {'ordering': "(u'group', u'title')", 'object_name': 'ImageMap'},
            'auto_from_above': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_geo_direction': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_geo_polygon': ('django.db.models.fields.CharField', [], {'default': "u'270000,570000,270000,580000,280000,580000,280000,570000'", 'max_length': '200'}),
            'auto_offset_x': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_offset_y': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_scale_x': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'auto_scale_y': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'auto_scale_z': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.ImageMapGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemapgroup': {
            'Meta': {'ordering': "(u'index', u'title')", 'object_name': 'ImageMapGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemaplink': {
            'Meta': {'ordering': "(u'image_map_index',)", 'object_name': 'ImageMapLink'},
            'coords': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.ImageMap']"}),
            'image_map_index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geodin.Measurement']", 'null': 'True', 'blank': 'True'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.Segment']", 'null': 'True', 'blank': 'True'}),
            'shape': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.informationpointer': {
            'Meta': {'object_name': 'InformationPointer'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'more_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.link': {
            'Meta': {'ordering': "(u'title',)", 'object_name': 'Link'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.linkset': {
            'Meta': {'object_name': 'LinkSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.Link']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.message': {
            'Meta': {'ordering': "(u'timestamp',)", 'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.MessageTag']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'lizard_levee.messagebox': {
            'Meta': {'object_name': 'MessageBox'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.MessageTag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.messagetag': {
            'Meta': {'object_name': 'MessageTag'},
            'html_color': ('django.db.models.fields.CharField', [], {'default': "u'black'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'lizard_levee.segment': {
            'Meta': {'object_name': 'Segment'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'segments'", 'null': 'True', 'to': "orm['lizard_levee.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poly': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'risk': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'segment_id': ('django.db.models.fields.IntegerField', [], {})
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
            'show_legend': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lizard_levee']
