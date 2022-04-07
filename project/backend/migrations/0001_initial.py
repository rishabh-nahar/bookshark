# Generated by Django 4.0.1 on 2022-04-06 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='listing_books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(default=None, max_length=70)),
                ('book_author', models.CharField(default=None, max_length=70)),
                ('book_publisher', models.CharField(default=None, max_length=70)),
                ('book_year_edition', models.IntegerField(default=None, null=True)),
                ('book_selling_price', models.CharField(default=None, max_length=70)),
                ('book_description', models.CharField(default=None, max_length=1000)),
            ],
            options={
                'db_table': 'book_details',
            },
        ),
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('unique_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=6)),
                ('mail', models.CharField(max_length=50, unique=True)),
                ('phone', models.BigIntegerField(default=None)),
                ('username', models.CharField(default=None, max_length=30, unique=True)),
                ('password', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_faculty', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_content_writer', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='file_upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(default=None, max_length=6)),
                ('file_name', models.CharField(default=None, max_length=50)),
                ('file_url', models.CharField(default=None, max_length=200)),
                ('category', models.CharField(default=None, max_length=40)),
                ('is_appropriate', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend.user_details', verbose_name='user_unique_id')),
            ],
            options={
                'db_table': 'file_details',
            },
        ),
    ]
