# Generated by Django 2.2.3 on 2019-07-18 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190716_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftedcoins',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='giftedcoins',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='spentcoins',
            name='sender',
        ),
        migrations.DeleteModel(
            name='EarnedCoins',
        ),
        migrations.DeleteModel(
            name='GiftedCoins',
        ),
        migrations.DeleteModel(
            name='SpentCoins',
        ),
    ]
