# Generated by Django 2.1.4 on 2019-03-15 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('howdy', '0012_ad_daily_report_two'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_extruder_waste',
            name='report_date',
            field=models.DateField(default=datetime.date(2019, 3, 15)),
        ),
    ]
