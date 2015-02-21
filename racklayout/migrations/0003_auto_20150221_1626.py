# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('racklayout', '0002_auto_20150221_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='row',
            old_name='dcid',
            new_name='dc',
        ),
    ]
