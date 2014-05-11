import json
import urllib
import urllib2

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _


class Municipality(models.Model):
    name = models.CharField(max_length=254)
    province = models.ForeignKey('Province', null=True, blank=True)

    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


    class Meta:
        verbose_name_plural = _(u'municipalities')

    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        else:
            return u'Municipality-%2d' % self.pk

    def get_floodmaps(self):
        # fetch floodmaps list from NOAH
        flooding_events = urllib2.urlopen('http://202.90.153.89/api/flood_maps')
        flooding_events = flooding_events.read()
        flooding_events = json.loads(flooding_events)

        geoserver_layers = []
        for event in flooding_events:
            if event['verbose_name'] == '100-Year':
                floods = event['flood']

                for flood in floods:
                    flood_center = flood['center']
                    flood_center = Point(flood_center['lng'], flood_center['lat'])
                    if self.geom.contains(flood_center):
                        geoserver_layers.append(flood['geoserver_layer'])

        print geoserver_layers

        # fetch *.kml files from NOAH

        return []


# Auto-generated `LayerMapping` dictionary for Municipality model
municipality_mapping = {
    'name' : 'MUNICIPALI',
    'province_name': 'PROVINCE',
    'geom' : 'MULTIPOLYGON',
}


class Province(models.Model):
    name = models.CharField(max_length=254)
    region = models.ForeignKey('Region', null=True, blank=True)

    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        else:
            return u'Province-%2d' % self.pk

# Auto-generated `LayerMapping` dictionary for Province model
province_mapping = {
    'name' : 'PROVINCE',
    'region_name': 'REGION',
    'region_desc': 'REG_DESC',
    'geom' : 'MULTIPOLYGON',
}


class Region(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)

    def __unicode__(self):
        return u'%s' % self.name
