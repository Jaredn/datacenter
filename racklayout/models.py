from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.core.validators import RegexValidator
# non django imports
from model_utils import Choices
# Create your models here.
# todo: label should have a regext to accept hostnames of devices and the convention for patch panels


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
        label: (str) ASH -> 3 letter code

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
        ordering = ('metro__label', 'number')
        # migration tool will insert a constraint in DB
        unique_together = ('number', 'metro')

    def __unicode__(self):
        return '%s%d' % (self.metro.label, self.number)


class Row(BaseModel):
    """
    class for a row in a data center
    :param
        label: (str) example F or 10
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
        unique_together = ('dc', 'label')

    def __unicode__(self):
        return '%s' % self.label

    def get_absolute_url(self):
        return reverse('racklayout:dc', kwargs={'dcid': self.dc_id})

class HalfUnit(BaseModel):
    """
    class for the units in a rack. A rack unit is split into two parts
    front and back. This allows to assets that have a half rack depth
    to support assets in the front and patch panels in the back or
    vice versa
    """
    PARTS = Choices((0,'front'), (1,'back'))
    asset = models.ForeignKey('Asset', null=True , default=None, related_name='units')
    location = models.IntegerField()
    # HalfUnit.PARTS.front
    part = models.IntegerField(choices=PARTS)
    rack = models.ForeignKey('Rack', default=None, related_name='units')

    class Meta:
        ordering = ('-location', 'asset')
        unique_together = ('rack', 'location', 'part')

    def __unicode__(self):
        return '%s, %s, %s' % (self.asset, self.location, self.PARTS[self.part])


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
    row = models.ForeignKey(Row, related_name='racks')
    totalunits = models.IntegerField(default=48)

    class Meta:
        ordering = ('row',)

    def save(self, *args, **kwargs):

        super(Rack, self).save(*args, **kwargs)

        for unit in range(1, self.totalunits+1):
            HalfUnit.objects.create(location=unit, rack=self, part=0)
            HalfUnit.objects.create(location=unit, rack=self, part=1)


    def __unicode__(self):
        return '%s%s' % (self.row.label, self.label)

    def get_absolute_url(self):
        return reverse('racklayout:dc', kwargs={'dcid': self.row.dc_id})

class Asset(BaseModel):
    """
    class for assets that are in our rack
    possible assets
        patch panel
        server
        network device
        console device
    :param
        :ASSET_TYPES
        :hostname
        :asset_type
    """
    ASSET_TYPES = Choices((0, 'server'), (1, 'panel'), (2, 'network'), (3, 'console'))

    label = models.CharField(max_length=64)
    asset_type = models.IntegerField(choices=ASSET_TYPES)

    # class Meta:
    #     unique_together = ('label', 'rack')

    def __unicode__(self):
        return '%s' % self.label

    # todo this needs to be fixed
    #def get_absolute_url(self):
    #    return reverse('racklayout:rack', kwargs={'pk': self.units.all()[0].rack_id})
