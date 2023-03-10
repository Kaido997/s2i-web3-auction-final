# Generated by Django 4.1.3 on 2023-01-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micromobility', '0011_alter_auction_auctionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auctionId',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='auction',
            name='ethTx',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='auction',
            name='finalPrice',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='initPrice',
            field=models.PositiveIntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(choices=[('c', 'CLOSE'), ('o', 'OPEN')], max_length=32),
        ),
    ]
