# Generated by Django 2.1.4 on 2019-03-15 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('howdy', '0013_auto_20190315_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='isAdstar',
        ),
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='payment_currency',
        ),
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='payment_time_tolerance',
        ),
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='payment_way',
        ),
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='sales_manager_agreement',
        ),
        migrations.RemoveField(
            model_name='productio_order_test2',
            name='total_price',
        ),
    ]