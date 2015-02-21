# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('racklayout', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dc',
            options={'ordering': ('metro__label', 'number')},
        ),
        migrations.AddField(
            model_name='dc',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='dc',
            unique_together=set([('number', 'metro')]),
        ),
        migrations.RemoveField(
            model_name='dc',
            name='label',
        ),
    ]
