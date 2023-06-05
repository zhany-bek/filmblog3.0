# Generated by Django 4.2.1 on 2023-06-05 05:21

from django.db import migrations, models
import films.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('director_name', models.CharField(max_length=100, null=True)),
                ('release_year', models.PositiveIntegerField(null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to=films.models.poster_upload_to)),
                ('description', models.TextField(blank=True)),
                ('rating', models.FloatField(null=True)),
            ],
        ),
    ]