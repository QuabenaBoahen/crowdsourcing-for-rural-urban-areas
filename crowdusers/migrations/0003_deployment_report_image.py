# Generated by Django 3.0.5 on 2020-06-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdusers', '0002_deployment'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='report_image',
            field=models.ImageField(blank=True, upload_to='deployment/images/'),
        ),
    ]