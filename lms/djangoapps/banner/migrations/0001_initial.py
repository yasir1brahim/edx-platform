# Generated by Django 2.2.18 on 2021-04-20 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_overviews', '0038_merge_20210405_0536'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_img_url_txt', models.TextField(blank=True, default='')),
                ('banner_img', models.ImageField(upload_to='banner/lms/courses')),
                ('enabled', models.BooleanField(default=True)),
                ('platform', models.CharField(choices=[('mobile', 'MOBILE'), ('web', 'WEB'), ('both', 'BOTH')], max_length=10)),
                ('slide_position', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('course_over_view', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_over_view', to='course_overviews.CourseOverview')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
