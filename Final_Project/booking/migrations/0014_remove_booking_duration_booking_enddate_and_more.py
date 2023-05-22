# Generated by Django 4.2.1 on 2023-05-22 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_rename_availabledates_availabledate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='duration',
        ),
        migrations.AddField(
            model_name='booking',
            name='enddate',
            field=models.DateField(default=datetime.date(2023, 5, 22)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='startdate',
            field=models.DateField(default=datetime.date(2023, 5, 22)),
            preserve_default=False,
        ),
    ]