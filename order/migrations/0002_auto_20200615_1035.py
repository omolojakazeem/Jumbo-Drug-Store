# Generated by Django 3.0.6 on 2020-06-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugorderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
