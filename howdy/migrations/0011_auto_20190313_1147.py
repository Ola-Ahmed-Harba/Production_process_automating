# Generated by Django 2.1.4 on 2019-03-13 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('howdy', '0010_auto_20190313_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad_daily_report_two',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='ad_daily_report_two',
            name='report_id',
        ),
        migrations.DeleteModel(
            name='AD_daily_report_two',
        ),
    ]
