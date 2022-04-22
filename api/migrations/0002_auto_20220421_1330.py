# Generated by Django 3.2.12 on 2022-04-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('tags', models.CharField(max_length=200)),
                ('recipe', models.TextField()),
                ('image', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Chef',
        ),
    ]
