# Generated by Django 4.1.5 on 2023-03-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mriic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
