# Generated by Django 2.2.2 on 2019-07-08 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='realtor_email',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
