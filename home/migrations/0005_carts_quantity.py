# Generated by Django 3.0.5 on 2020-06-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_carts'),
    ]

    operations = [
        migrations.AddField(
            model_name='carts',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
