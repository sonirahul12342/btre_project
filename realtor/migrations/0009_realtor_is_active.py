# Generated by Django 2.2.2 on 2019-07-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtor', '0008_auto_20190705_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtor',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
