# Generated by Django 3.0.5 on 2020-06-09 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_items_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
