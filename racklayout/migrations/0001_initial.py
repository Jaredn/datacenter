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
                ('asset_type', models.IntegerField(choices=[(0, b'server'), (1, b'panel'), (2, b'network'), (3, b'console')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
            ],
            options={
                'ordering': ('metro__label', 'number'),
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
                ('asset', models.ForeignKey(related_name='units', default=None, to='racklayout.Asset')),
            ],
            options={
                'ordering': ('-location', 'asset'),
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
                ('dc', models.ForeignKey(to='racklayout.Dc')),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='row',
            unique_together=set([('dc', 'label')]),
        ),
        migrations.AddField(
            model_name='rack',
            name='row',
            field=models.ForeignKey(related_name='racks', to='racklayout.Row'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='halfunit',
            name='rack',
            field=models.ForeignKey(related_name='units', default=None, to='racklayout.Rack'),
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
        migrations.AlterUniqueTogether(
            name='dc',
            unique_together=set([('number', 'metro')]),
        ),
    ]
