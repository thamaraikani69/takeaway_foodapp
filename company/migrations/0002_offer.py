# Generated by Django 3.2.6 on 2021-12-30 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateField()),
                ('offer_name', models.TextField()),
                ('offer_percentage', models.IntegerField()),
                ('times', models.BigIntegerField()),
                ('status', models.TextField()),
                ('last_change', models.DateTimeField()),
            ],
        ),
    ]