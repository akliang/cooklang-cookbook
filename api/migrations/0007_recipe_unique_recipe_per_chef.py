# Generated by Django 3.2.13 on 2022-04-26 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_bookmarks_bookmark'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('chef', 'title'), name='unique_recipe_per_chef'),
        ),
    ]