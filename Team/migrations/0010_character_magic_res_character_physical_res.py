# Generated by Django 4.2.4 on 2023-09-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0009_character_last_purchase_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='magic_res',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='character',
            name='physical_res',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
