# Generated by Django 4.2.4 on 2023-10-14 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0011_alter_inventoryitem_constitution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='shop_type',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
