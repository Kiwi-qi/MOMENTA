# Generated by Django 2.0.4 on 2019-07-02 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0002_auto_20190702_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowconf',
            name='creater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]