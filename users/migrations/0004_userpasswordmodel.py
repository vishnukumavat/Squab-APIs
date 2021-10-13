# Generated by Django 3.2.8 on 2021-10-13 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_usersmodel_country_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extra_details', models.JSONField(blank=True, default=dict, null=True)),
                ('password', models.CharField(editable=False, max_length=512, null=True)),
                ('otp', models.IntegerField(editable=False, null=True)),
                ('is_otp_verified', models.BooleanField(default=False, null=True)),
                ('otp_created_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.usersmodel')),
            ],
            options={
                'db_table': 'user_password',
            },
        ),
    ]
