# Generated by Django 2.1.4 on 2019-03-02 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('howdy', '0004_auto_20190302_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificate',
            name='recipient',
        ),
        migrations.DeleteModel(
            name='notificate',
        ),
    ]
