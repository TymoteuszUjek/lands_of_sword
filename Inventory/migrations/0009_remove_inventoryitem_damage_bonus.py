# Generated by Django 4.2.4 on 2023-09-14 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0008_inventoryitem_damage_bonus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='damage_bonus',
        ),
    ]
