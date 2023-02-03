# Generated by Django 4.1.3 on 2023-01-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micromobility', '0007_alter_auction_finalprice_alter_auction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_start',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='item',
            field=models.CharField(default=None, max_length=32),
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(default='open', max_length=16),
        ),
    ]