# Generated by Django 2.2.5 on 2020-02-14 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_reper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ManyToManyField(related_name='image_reper', to='core.Image')),
            ],
        ),
    ]