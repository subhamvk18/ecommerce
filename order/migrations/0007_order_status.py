# Generated by Django 3.0.5 on 2020-06-10 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200610_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='initiate', max_length=100),
        ),
    ]