# Generated by Django 4.1.7 on 2023-03-12 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_out',
            field=models.DateTimeField(),
        ),
    ]
