# Generated by Django 2.2.6 on 2020-02-14 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200214_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='extra_images',
        ),
        migrations.DeleteModel(
            name='ExtraImages',
        ),
    ]
