# Generated by Django 3.2.8 on 2021-10-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmodel',
            name='profile_pic_link',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
