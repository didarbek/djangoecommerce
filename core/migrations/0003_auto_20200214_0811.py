# Generated by Django 2.2.6 on 2020-02-14 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200214_0749'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sex',
            options={'ordering': ('name',), 'verbose_name': 'sex', 'verbose_name_plural': 'sexes'},
        ),
    ]
