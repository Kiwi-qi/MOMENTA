# Generated by Django 2.0.4 on 2019-07-02 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flowconf',
            old_name='desciription',
            new_name='description',
        ),
    ]
