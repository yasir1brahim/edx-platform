# Generated by Django 2.2.15 on 2020-12-23 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_squashed_0007_historicalorganization'),
        ('custom_reg_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextrainfo',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instructor_org', to='organizations.Organization'),
        ),
    ]
