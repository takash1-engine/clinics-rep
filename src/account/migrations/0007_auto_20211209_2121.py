# Generated by Django 3.0.4 on 2021-12-09 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210705_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='carrer',
            new_name='career',
        ),
    ]
