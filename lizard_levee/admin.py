# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import math
import logging
import twitter

# from django.utils.translation import ugettext as _
from django.contrib.gis import admin
from sorl.thumbnail.admin import AdminImageMixin

from lizard_levee import models
from lizard_geodin.models import Point

logger = logging.getLogger(__name__)


class ImageMapLinkInline(admin.TabularInline):
    model = models.ImageMapLink


class AreaAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('wms_layers', 'information_pointers', 'links')


class InformationPointerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('slug', 'title', 'more_url')
    list_editable = ('title', 'more_url')
    prepopulated_fields = {"slug": ("title",)}


class LinkSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    list_editable = ('title', 'url')


class SegmentAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'area', 'segment_id', 'risk')
    list_editable = ('risk',)


# Got from internet, it uses the crossing number algorithm.
# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


def point_in_poly(poly):
    """Return a function that determines for a geodin Point object if
    it's in the given polygon.
    """
    def fun(point):
        return point_inside_polygon(point.x, point.y, poly)
    return fun


def rotate_point(direction):
    cos_theta = math.cos(direction)
    sin_theta = math.sin(direction)
    def fun(p):
        x_new = p[0] * cos_theta - p[1] * sin_theta
        y_new = p[0] * sin_theta + p[1] * cos_theta
        return (x_new, y_new, p[2], p[3])
    return fun


class ImageMapAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'group')
    prepopulated_fields = {"slug": ("title", )}
    inlines = [ImageMapLinkInline, ]

    actions = ['generate_image_map_delete_existing',
               'generate_image_map_add_outer_points',
               'generate_image_map_test',
               'duplicate']

    def duplicate(self, request, queryset):
        num_created = 0
        for image_map in queryset:
            new_object = models.ImageMap(
                title=image_map.title + ' copy',
                slug=image_map.slug + '-',
                image_url=image_map.image_url,
                image_width=image_map.image_width,
                image_height=image_map.image_height,
                image_scale=image_map.image_scale,
                group=image_map.group,
                auto_geo=image_map.auto_geo,
                auto_geo_polygon=image_map.auto_geo_polygon,
                auto_from_above=image_map.auto_from_above,
                auto_geo_direction=image_map.auto_geo_direction,
                auto_scale_x=image_map.auto_scale_x,
                auto_scale_y=image_map.auto_scale_y,
                auto_scale_z=image_map.auto_scale_z,
                auto_offset_x=image_map.auto_offset_x,
                auto_offset_y=image_map.auto_offset_y,
                auto_grouping_size=image_map.auto_grouping_size)
            new_object.save()
            num_created += 1
        return self.message_user(
            request,
            'Finished, Created: %d' % (num_created))

    def generate_image_map_add_outer_points(self, request, queryset):
        return self.generate_image_map(request, queryset, delete_old=True, add_outer_points=True)

    def generate_image_map_add_to_existing(self, request, queryset):
        return self.generate_image_map(request, queryset, delete_old=False)

    def generate_image_map_delete_existing(self, request, queryset):
        return self.generate_image_map(request, queryset, delete_old=True)

    def generate_image_map_test(self, request, queryset):
        return self.generate_image_map(request, queryset, test=True)

    def generate_image_map(self, request, queryset, delete_old=False, test=False, add_outer_points=False):
        """
        Generate image map link objects, using all parameters
        ImageMap.auto*

        Test messages appear as warnings, because they are then showed
        on the production server.
        """
        logger.info('Generate image map')
        min_x, max_x, min_y, max_y = None, None, None, None
        skipped = 0
        added = 0
        moved = 0
        for image_map in queryset:
            # Get all the points
            if test:
                # make points on the corner of the poly
                coords = image_map.auto_poly
                points = [Point(x=cx, y=cy, z=i%2) for i, (cx, cy) in enumerate(coords)]
                # make them appear in the log
                logger.warning('Testing coords: %r' % coords)
            else:
                points = Point.objects.all()

            # Filter points that are inside the polygon.
            if image_map.auto_poly is not None and not test:
                points_in_poly = filter(point_in_poly(image_map.auto_poly), points)
            else:
                points_in_poly = points  # All of 'em for testing purposes.

            for point in points_in_poly:
                logger.info('Point in poly: %r %r %s' % (point.x, point.y, point))

            # Rotate and map on image
            #center_x, center_y = image_map.auto_center
            moved_points = [(p.x, p.y, p.z, p) for p in points_in_poly]

            scaled_points = [(p[0]*image_map.auto_scale_x,
                              p[1]*image_map.auto_scale_y,
                              p[2]*image_map.auto_scale_z,
                              p[3]) for p in moved_points]

            rotated_points = map(
                rotate_point(image_map.auto_direction_radian), scaled_points)

            if image_map.auto_from_above:
                # Top view
                # screen_x = y, screen_y = x
                offset_points = [(p[0]+image_map.auto_offset_x,
                                  p[1]+image_map.auto_offset_y,
                                  0,
                                  p[3]) for p in rotated_points]

            else:
                # Front view:
                # screen_x = y, x and screen_y=z
                offset_points = [(p[1]+image_map.auto_offset_x,
                                  p[2]+image_map.auto_offset_y,
                                  0,
                                  p[3]) for p in rotated_points]

            # Now update the image map
            if delete_old:
                image_map.imagemaplink_set.all().delete()

            saved_image_map_links = {}  # (keys are x,y coords rounded by 10)
            # Check if points are to be grouped together
            for x, y, z, p in offset_points:
                if x > -10 and y > -10 and x < image_map.image_width + 10 and y < image_map.image_height + 10:
                    key = (int(x)/image_map.auto_grouping_size, int(y)/image_map.auto_grouping_size)
                    if key not in saved_image_map_links:
                        saved_image_map_links[key] = []
                    saved_image_map_links[key].append((x,y,z,p))
                    # title = '%s (%r, %r, %r)' % (str(p), p.x, p.y, p.z)
                    # image_map_link = image_map.imagemaplink_set.create(
                    #     title=title,
                    #     shape='circle',
                    #     coords='%d,%d,5' % (int(x), int(y))
                    #     )
                    # image_map_link.points.add(p)
                    added += 1
                else:
                    if add_outer_points:
                        moved += 1
                        if x < 0:
                            x = 0
                        if x > image_map.image_width:
                            x = image_map.image_width
                        if y < 0:
                            y = 0
                        if y > image_map.image_height:
                            y = image_map.image_height

                        key = (int(x)/image_map.auto_grouping_size, int(y)/image_map.auto_grouping_size)
                        if key not in saved_image_map_links:
                            saved_image_map_links[key] = []
                        saved_image_map_links[key].append((x,y,z,p))
                    else:
                        skipped += 1
                if min_x is None or x < min_x:
                    min_x = x
                if min_y is None or y < min_y:
                    min_y = y
                if max_x is None or x > max_x:
                    max_x = x
                if max_y is None or y > max_y:
                    max_y = y

            if not test:
                # Now add grouped items to image map links
                for k, v in saved_image_map_links.items():
                    if len(v) == 1:
                        # Single point
                        x, y, z, p = v[0]
                        title = '%s (%f %f %f)' % (str(p), p.x, p.y, p.z)
                        image_map_link = image_map.imagemaplink_set.create(
                            title=title,
                            shape='circle',
                            coords='%d,%d,5' % (int(x), int(y)),
                            color_me=False
                            )
                        image_map_link.points.add(p)
                    else:
                        # Multipoint
                        x, y, z, p = v[0]
                        #title = '%s' % (', '.join([str(pp[3]) for pp in v]))
                        title = "Meervoudig punt (%f %f %f)" % (p.x, p.y, p.z)
                        image_map_link = image_map.imagemaplink_set.create(
                            title=title,
                            shape='circle',
                            coords='%d,%d,7' % (int(x), int(y)),
                            color_me=False
                            )
                        for _x, _y, _z, _p in v:
                            image_map_link.points.add(_p)

        # try:
        #     suggestion = 'Suggestion for sideview: auto_scale_y=%r' % (image_map.image_width/(max_x - min_x))
        # except:
        #     suggestion = 'No suggestion'

        try:
            diff_x = max_x - min_x
        except:
            diff_x = '?'
        try:
            diff_y = max_y - min_y
        except:
            diff_y = '?'

        return self.message_user(
            request,
            'Finished, screen(min,max,diff) x(%r %r %r), y(%r %r %r). Added: %d, Moved: %d, Skipped: %d' % (
                min_x, max_x, diff_x, min_y, max_y, diff_y, added, moved, skipped))


class MessageTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"tag": ("name",)}


class MessageBoxAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    actions = ['repopulate_twitter_feed']

    def repopulate_twitter_feed(self, request, queryset):
        logger.info('Harvesting...')
        tag = models.MessageTag.objects.get(tag='twitter')
        models.Message.objects.filter(tags__tag='twitter').delete()
        twitter_search = twitter.Twitter(domain="search.twitter.com")
        tw_result = twitter_search.search(q="#ijkdijk")
        message_count = 0
        for result in tw_result['results']:
            message_txt = '%s: %s' % (result['from_user_name'], result['text'])
            message = models.Message(message=message_txt)
            message.save()
            message.tags.add(tag)
            logger.info(message_txt)
            message_count += 1
        logger.info('Done')
        return self.message_user(
            request,
            'Added %d twitter messages' % message_count)


class PointSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MessageAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'message', 'tags_str']


class ImageMapGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'index', 'title']
    list_editable = ('index', 'title')


admin.site.register(models.MessageTag, MessageTagAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.MessageBox, MessageBoxAdmin)

admin.site.register(models.ImageMapGroup, ImageMapGroupAdmin)
admin.site.register(models.ImageMap, ImageMapAdmin)
admin.site.register(models.ImageMapGeoPolygon)

admin.site.register(models.Link, LinkAdmin)
admin.site.register(models.LinkSet, LinkSetAdmin)

admin.site.register(models.PointSet, PointSetAdmin)

admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.InformationPointer, InformationPointerAdmin)
admin.site.register(models.Segment, SegmentAdmin)

admin.site.register(models.UploadedFile)
