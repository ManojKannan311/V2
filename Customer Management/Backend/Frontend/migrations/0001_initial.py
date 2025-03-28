# Generated by Django 5.1.6 on 2025-03-15 05:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catogery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_ID', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('Email_id', models.EmailField(max_length=255)),
                ('address', models.TextField()),
                ('Enquiry_details', models.TextField()),
                ('age', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=50)),
                ('Requried_date', models.DateField(blank=True, null=True)),
                ('Reminder_date', models.DateField(blank=True, null=True)),
                ('Product_Price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Payment', models.CharField(max_length=50)),
                ('added_by', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('Feed_back', models.TextField(blank=True, null=True)),
                ('Remainder_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incentive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_id', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_address', models.TextField()),
                ('customer_mobile_no', models.CharField(max_length=15)),
                ('product_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('courier_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=60)),
                ('handled_staff_name', models.CharField(max_length=100)),
                ('courier_id', models.CharField(max_length=100)),
                ('couriered_date', models.DateField(auto_now=True)),
                ('product_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('Role', models.CharField(max_length=50)),
                ('New_pass', models.CharField(max_length=20)),
                ('DOB', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='Frontend.catogery')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_status', models.CharField(blank=True, max_length=50)),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('Customer_feedback', models.TextField(blank=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontend.staff')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontend.customer')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Frontend.user_details'),
        ),
        migrations.AddField(
            model_name='customer',
            name='Staff_Assign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Staff_name', to='Frontend.user_details'),
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_id', models.CharField(max_length=50, unique=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('product_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('courier_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=3)),
                ('courier_id', models.CharField(max_length=50)),
                ('couriered_date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontend.user_details')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin_manager', 'Admin Manager'), ('support_team', 'Support Team'), ('finance_manager', 'Finance Manager')], default='admin_manager', max_length=50)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('new_pass', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
