# Generated by Django 3.2.3 on 2021-06-16 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petitions', '0002_auto_20210616_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petitionsignature',
            name='signator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
