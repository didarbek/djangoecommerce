# Generated by Django 2.2.6 on 2020-02-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200212_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='short_description',
            field=models.CharField(blank=True, max_length=38, null=True),
        ),
    ]
