# Generated by Django 4.1.4 on 2023-05-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_message_listing_comment_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=150),
        ),
    ]
