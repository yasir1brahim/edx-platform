# Generated by Django 2.2.20 on 2021-05-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lhub_ecommerce_offer', '0008_auto_20210520_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='name',
            field=models.CharField(default='ABC', max_length=250),
            preserve_default=False,
        ),
    ]
