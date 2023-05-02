# Generated by Django 4.1.5 on 2023-05-01 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_alter_attendance_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
    ]
