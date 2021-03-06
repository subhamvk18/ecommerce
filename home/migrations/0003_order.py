# Generated by Django 3.0.5 on 2020-06-05 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_category_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('etime', models.DateTimeField()),
                ('cost', models.IntegerField()),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('Items', models.ManyToManyField(to='home.Items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
