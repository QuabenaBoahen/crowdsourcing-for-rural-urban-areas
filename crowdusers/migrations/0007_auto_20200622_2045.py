# Generated by Django 3.0.5 on 2020-06-22 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdusers', '0006_auto_20200622_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='deployment_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]