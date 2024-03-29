# Generated by Django 2.2.3 on 2019-07-21 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0005_auto_20190721_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkstatelog',
            name='approved_transactions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='networkstatelog',
            name='last_network_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
