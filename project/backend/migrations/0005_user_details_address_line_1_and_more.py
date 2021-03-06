# Generated by Django 4.0.1 on 2022-05-01 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_user_details_address_pincode_delete_file_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='address_line_1',
            field=models.CharField(default=None, max_length=1024),
        ),
        migrations.AddField(
            model_name='user_details',
            name='address_line_2',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='user_details',
            name='city',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='user_details',
            name='state',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
