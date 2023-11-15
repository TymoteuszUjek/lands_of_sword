# Generated by Django 4.2.4 on 2023-10-14 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Items', '0013_item_shop_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_count', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carpentry_shop_transactions', to='Items.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carpentry_shop_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
