# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Message.image_url'
        db.add_column('lizard_levee_message', 'image_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Message.image_url'
        db.delete_column('lizard_levee_message', 'image_url')


    models = {
        'lizard_geodin.apistartingpoint': {
            'Meta': {'object_name': 'ApiStartingPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_geodin.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'data_type_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigation_type_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'location_type_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.Parameter']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.Project']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'measurements'", 'null': 'True', 'to': "orm['lizard_geodin.Supplier']"})
        },
        'lizard_geodin.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'lizard_geodin.point': {
            'Meta': {'ordering': "(u'name', u'slug')", 'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'points'", 'null': 'True', 'to': "orm['lizard_geodin.Measurement']"}),
            'metadata': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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
        'lizard_geodin.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'html_color': ('django.db.models.fields.CharField', [], {'default': "u'#444444'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
            'auto_geo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.ImageMapGeoPolygon']", 'null': 'True', 'blank': 'True'}),
            'auto_geo_direction': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_geo_polygon': ('django.db.models.fields.CharField', [], {'default': "u'270000,570000,270000,580000,280000,580000,280000,570000'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'auto_grouping_size': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'auto_offset_x': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_offset_y': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'auto_scale_x': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'auto_scale_y': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'auto_scale_z': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.ImageMapGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'default': '250'}),
            'image_scale': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'default': '800'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemapgeopolygon': {
            'Meta': {'object_name': 'ImageMapGeoPolygon'},
            'geo_polygon': ('django.db.models.fields.CharField', [], {'default': "u'270000,570000,270000,580000,280000,580000,280000,570000'", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemapgroup': {
            'Meta': {'ordering': "(u'index', u'title')", 'object_name': 'ImageMapGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'lizard_levee.imagemaplink': {
            'Meta': {'ordering': "(u'image_map_index',)", 'object_name': 'ImageMapLink'},
            'color_me': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coords': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_levee.ImageMap']"}),
            'image_map_index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geodin.Measurement']", 'null': 'True', 'blank': 'True'}),
            'points': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_geodin.Point']", 'null': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "(u'-timestamp',)", 'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_levee.MessageTag']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
        'lizard_levee.pointset': {
            'Meta': {'ordering': "(u'index',)", 'object_name': 'PointSet'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_geodin.Point']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '500'})
        },
        'lizard_levee.segment': {
            'Meta': {'object_name': 'Segment'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'segments'", 'null': 'True', 'to': "orm['lizard_levee.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poly': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'risk': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'segment_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'lizard_levee.uploadedfile': {
            'Meta': {'object_name': 'UploadedFile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uploaded_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
