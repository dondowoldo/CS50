# Generated by Django 4.1.4 on 2023-05-15 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_propertytypes_remove_listing_property_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PropertyTypes',
            new_name='PropertyType',
        ),
    ]
