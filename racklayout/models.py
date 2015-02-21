from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import RegexValidator
#### non django imports


# Create your models here.
from model_utils import Choices


class BaseModel(models.Model):
    """
    an abstract base class model that provides  self-updating
     'created' and 'modified' fields, as well as generic fields that
     each class uses like name.
     :param
        created: datetime
        modified: datetime
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Metro(BaseModel):
    """
    class for metro
    :param
        lable: (str) ASH -> 3 letter code

    validation rules:
        must be unique
        must be 3  capital letter code
    """
    label = models.CharField(max_length=3,
                             unique=True,
                             validators=[
                                 RegexValidator(
                                     regex='^[A-Z]{3}',
                                     message='Metro must be 3  capital letters',
                                     code='invalid_metro'
                                 ),
                             ]
                             )

    def __unicode__(self):
        return '%s' % self.label


class Dc(BaseModel):
    """
    class for dc
    :param
        label: (str) ASH1 -> 3 letter code followed by a number
        metroid: ForeignKey to metro

    validation rules:
        must be unique
        must be a three capital letter code followed by a number
    """
    number = models.IntegerField()
    metro = models.ForeignKey(Metro)

    class Meta:
        ordering = ('metro__label','number')
        # migration tool will insert a constraint in DB
        unique_together = ('number', 'metro')

    def __unicode__(self):
        return '%s%d' % (self.metro.label, self.number)


class Row(BaseModel):
    """
    class for a row in a data center
    :param
        label: (str) exmaple F or 10
    """
    dc = models.ForeignKey(Dc)
    label = models.CharField(max_length=3,
                             unique=False,
                             validators=[
                                 RegexValidator(
                                     regex='^[A-Z]+$|^\d+$',
                                     message='Row is either letters or number not both',
                                     code='invalid_row'
                                 )
                             ]
                             )

    class Meta:
        ordering = ('label',)

    def __unicode__(self):
        return '%s' % self.label

class Rack(BaseModel):
    """
    class for rack
    :param
        label: (str) a letter or a number
        dcid: ForeignKey to DC
        totalunits: (int) number of rack units in rack

    validation rules

    """
    label = models.CharField(max_length=6,
                             unique=False,
                             validators=[
                                 RegexValidator(
                                     regex='^[A-Z]+$|^\d+$',
                                     message='Rack is either letters or number not both',
                                     code='ivalid_rack'
                                 )
                             ]
                             )
    row = models.ForeignKey(Row)
    totalunits = models.IntegerField(default=48)


    class Meta:
        ordering = ('row',)

    def __unicode__(self):
        return '%s' % self.label

class Asset(BaseModel):
    """
    class for assets that are in our rack
    possible assets
        patch panel
        server
        network device
        console device
    :param
        rackid: Forgienkey to Rack
        label: (str) free form text field
        rackunit: (int) this is the U location of the device (top u)
        unitsize: (int) size of asset
        front: (boolean): determines if the ass is in the front of the rack
        back: (boolean): determines if the asset is in the back of the rack
        power: (int) not sure how to calculate this
    """
    TYPES = Choices((0, 'server'), (1, 'patch_panel'), (3, 'network_device'))

    #todo add support for power calc per cabinet
    label = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPES)
    # rackid = models.ForeignKey(Rack)
    # rackunit = models.IntegerField()
    # unitsize = models.IntegerField()
    # front = models.BooleanField(default=False)
    # back = models.BooleanField(default=False)
    # panel = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ('rack',)
        # abstract = True

    def __unicode__(self):
        return '%s' % self.label


class HalfUnit(BaseModel):
    #
    # for rack in Rack.objects.filter(row__dcid=...):
    #   for unit rack.units:
    #
    PARTS = Choices((0, 'front'), (1, 'back'))
    rack = models.ForeignKey(Rack, related_name='units')
    location = models.IntegerField()
    # HalfUnit.PARTS.front
    part = models.IntegerField(choices=PARTS)

    # assets = Asset.objects.get(halfunit__rack=..).distinct()
    # for asset_type in types:
    #   TYPES[asset_type].objects.filter(pk__in=[....])

    front = models.BooleanField(default=False)
    # back = models.BooleanField(default=False)
    # asset = models.ForeignKey(Asset)

    # asset_id = models.PositiveIntegerField()
    # asset_content_type = models.ForeignKey(ContentType)
    # asset = GenericForeignKey('asset_content_type', 'asset_id')
    asset = models.ForeignKey(Asset)

    class Meta:
        # TODO: explain
        unique_together = ('rack', 'location', 'part')

    def __unicode__(self):
        return '%s, %s, %s' % (self.rackid, self.location, self.PARTS[self.part])

class PatchPanel(Asset):
    # parent_id =
    # label = models.CharField(max_length=64)
    pass

class Server(Asset):
    host_name = models.CharField(max_length=255)
    VENDORS = Choices((0, 'Dell'))
    vendor = models.IntegerField(choices=VENDORS)
    ip_address = models.IPAddressField()
    idrac = models.IPAddressField()

class NetworkDevice(Asset):
    host_name = models.CharField(max_length=255)
    VENDORS = Choices((0, 'Cisco'))
    vendor = models.IntegerField(choices=VENDORS)
    ip_address = models.IPAddressField()

class Port(BaseModel):
    """
    class for ports that are on our assets
    :param
        assetid: ForgienKey to Asset
        slot: (int) slot of port
        module: (int) module of port
        port: (int) port number
        front: (boolean) if the port is in the front or the back of the rack
    """
    patch_panel = models.ForeignKey(PatchPanel)

    # class Meta:
    #     ordering = ('port',)


class CrossConnects(BaseModel):
    """
    class for cross connects
    """
    aside = models.ForeignKey(Port, related_name='aside')
    zside = models.ForeignKey(Port, related_name='zside')

    class Meta:
        ordering = ('aside',)

# for r in Row.objects.filter(dcid=Dc.objects.all()[0]):
#     print r
#     for rack in Rack.objects.filter(row=r):
#         print '  ', rack
# In [24]: rows = defaultdict(set)
#
# In [25]: for rack in Rack.objects.filter(row__dcid=Dc.objects.all()[0]).select_related('row'):
#    ....:     rows[rack.row].add(rack)
