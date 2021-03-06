# Generated by Django 4.0.1 on 2022-04-13 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='book_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.URLField(blank=None)),
                ('book_uid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend.listing_books', verbose_name='book_id')),
            ],
            options={
                'db_table': 'book_images',
            },
        ),
    ]
