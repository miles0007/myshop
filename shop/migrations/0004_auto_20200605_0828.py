# Generated by Django 3.0.6 on 2020-06-05 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200605_0810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='featured',
        ),
    ]
