# Generated by Django 4.1.3 on 2022-12-06 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micromobility', '0003_alter_auction_item_alter_profile_favauctions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='favAuctions',
            new_name='watchList',
        ),
    ]