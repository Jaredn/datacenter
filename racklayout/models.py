from django.db import models
from django.core.validators import RegexValidator
#### non django imports


# Create your models here.


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
    label = models.CharField(max_length=4,
                             unique=True,
                             validators=[
                                 RegexValidator(
                                     regex='^[A-Z]{3}\d+',
                                     message='DC must be 3 capital letters followed by a number',
                                     code='invalid_dc'
                                 )
                             ]
                             )
    metroid = models.ForeignKey(Metro)

    class Meta:
        ordering = ('label',)

    def __unicode__(self):
        return '%s' % self.label


class Row(BaseModel):
    """
    class for a row in a data center
    :param
        label: (str) exmaple F or 10
    """
    dcid = models.ForeignKey(Dc)
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
    rowid = models.ForeignKey(Row)
    totalunits = models.IntegerField(default=48)


    class Meta:
        ordering = ('rowid',)

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
    #todo add support for power calc per cabinet
    rackid = models.ForeignKey(Rack)
    label = models.CharField(max_length=64)
    rackunit = models.IntegerField()
    unitsize = models.IntegerField()
    front = models.BooleanField(default=False)
    back = models.BooleanField(default=False)
    panel = models.BooleanField(default=False)

    class Meta:
        ordering = ('rackid',)

    def __unicode__(self):
        return '%s' % self.label


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
    assetid = models.ForeignKey(Asset)
    slot = models.IntegerField(null=True, blank=True)
    module = models.IntegerField(null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    front = models.BooleanField(default=False)

    class Meta:
        ordering = ('port',)


class CrossConnects(BaseModel):
    """
    class for cross connects
    """
    aside = models.ForeignKey(Port, related_name='aside')
    zside = models.ForeignKey(Port, related_name='zside')

    class Meta:
        ordering = ('aside',)
