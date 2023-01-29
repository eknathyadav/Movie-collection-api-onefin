# Generated by Django 4.1.5 on 2023-01-28 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestserve',
            name='requests_count',
        ),
        migrations.AddField(
            model_name='requestserve',
            name='endpoint',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='requestserve',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
