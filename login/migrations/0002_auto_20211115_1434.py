# Generated by Django 3.2.6 on 2021-11-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_login',
            name='picture',
            field=models.TextField(default=int),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_login',
            name='picture',
            field=models.TextField(default=int),
            preserve_default=False,
        ),
    ]