# Generated by Django 2.2.2 on 2019-07-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20190708_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
