# Generated by Django 5.1.6 on 2025-03-15 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0003_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('superadmin', 'SuperAdmin'), ('admin', 'Admin'), ('staff', 'Staff')], default='admin_manager', max_length=50),
        ),
    ]
