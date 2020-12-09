# Generated by Django 3.1.2 on 2020-11-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('update_ubike', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UbikeDistance',
            fields=[
                ('sno', models.IntegerField(primary_key=True, serialize=False)),
                ('distance', models.FloatField()),
            ],
            options={
                'db_table': 'ubike_distance',
            },
        ),
    ]