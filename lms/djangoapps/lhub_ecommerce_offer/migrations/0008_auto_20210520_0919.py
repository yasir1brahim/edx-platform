# Generated by Django 2.2.20 on 2021-05-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lhub_ecommerce_offer', '0007_auto_20210520_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='end_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end datetime'),
        ),
    ]
