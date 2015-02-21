# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=64)),
                ('type', models.IntegerField(choices=[(0, b'server'), (1, b'patch_panel'), (3, b'network_device')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrossConnects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('aside',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(unique=True, max_length=4, validators=[django.core.validators.RegexValidator(regex=b'^[A-Z]{3}\\d+', message=b'DC must be 3 capital letters followed by a number', code=b'invalid_dc')])),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HalfUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location', models.IntegerField()),
                ('part', models.IntegerField(choices=[(0, b'front'), (1, b'back')])),
                ('front', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(unique=True, max_length=3, validators=[django.core.validators.RegexValidator(regex=b'^[A-Z]{3}', message=b'Metro must be 3  capital letters', code=b'invalid_metro')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('asset_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='racklayout.Asset')),
                ('host_name', models.CharField(max_length=255)),
                ('vendor', models.IntegerField(choices=[(0, b'Cisco')])),
                ('ip_address', models.IPAddressField()),
            ],
            options={
                'abstract': False,
            },
            bases=('racklayout.asset',),
        ),
        migrations.CreateModel(
            name='PatchPanel',
            fields=[
                ('asset_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='racklayout.Asset')),
            ],
            options={
                'abstract': False,
            },
            bases=('racklayout.asset',),
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('patch_panel', models.ForeignKey(to='racklayout.PatchPanel')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex=b'^[A-Z]+$|^\\d+$', message=b'Rack is either letters or number not both', code=b'ivalid_rack')])),
                ('totalunits', models.IntegerField(default=48)),
            ],
            options={
                'ordering': ('row',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(regex=b'^[A-Z]+$|^\\d+$', message=b'Row is either letters or number not both', code=b'invalid_row')])),
                ('dcid', models.ForeignKey(to='racklayout.Dc')),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('asset_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='racklayout.Asset')),
                ('host_name', models.CharField(max_length=255)),
                ('vendor', models.IntegerField(choices=[(0, b'Dell')])),
                ('ip_address', models.IPAddressField()),
                ('idrac', models.IPAddressField()),
            ],
            options={
                'abstract': False,
            },
            bases=('racklayout.asset',),
        ),
        migrations.AddField(
            model_name='rack',
            name='row',
            field=models.ForeignKey(to='racklayout.Row'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='halfunit',
            name='asset',
            field=models.ForeignKey(to='racklayout.Asset'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='halfunit',
            name='rack',
            field=models.ForeignKey(related_name='units', to='racklayout.Rack'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='halfunit',
            unique_together=set([('rack', 'location', 'part')]),
        ),
        migrations.AddField(
            model_name='dc',
            name='metro',
            field=models.ForeignKey(to='racklayout.Metro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crossconnects',
            name='aside',
            field=models.ForeignKey(related_name='aside', to='racklayout.Port'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crossconnects',
            name='zside',
            field=models.ForeignKey(related_name='zside', to='racklayout.Port'),
            preserve_default=True,
        ),
    ]
