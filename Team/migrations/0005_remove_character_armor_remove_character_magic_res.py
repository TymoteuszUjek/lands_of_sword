# Generated by Django 4.2.4 on 2023-08-29 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0004_alter_character_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='armor',
        ),
        migrations.RemoveField(
            model_name='character',
            name='magic_res',
        ),
    ]
