# Generated by Django 3.0.5 on 2020-06-10 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Books', 'books'), ('Masks', 'mask'), ('Santizers', 'sanitizers'), ('Icecreams', 'icecreams')], max_length=200),
        ),
    ]
