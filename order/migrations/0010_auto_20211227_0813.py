# Generated by Django 3.2.9 on 2021-12-27 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20211224_1626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordercity',
            old_name='name',
            new_name='label',
        ),
        migrations.RenameField(
            model_name='ordercitysector',
            old_name='name',
            new_name='label',
        ),
    ]
