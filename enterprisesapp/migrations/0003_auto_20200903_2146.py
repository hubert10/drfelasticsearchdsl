# Generated by Django 2.2.13 on 2020-09-03 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprisesapp', '0002_auto_20200621_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='sectors',
            field=models.ManyToManyField(blank=True, related_name='enterprise_sectors', to='enterprisesapp.Sector'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='enterprise_skills', to='enterprisesapp.Skill'),
        ),
    ]
