# Generated by Django 4.1.1 on 2022-11-17 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
    ]
