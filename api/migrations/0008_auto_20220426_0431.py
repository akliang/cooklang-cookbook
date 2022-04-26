# Generated by Django 3.2.13 on 2022-04-26 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_recipe_unique_recipe_per_chef'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_per_chef',
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('chef', 'title', 'slug'), name='unique_recipe_per_chef'),
        ),
    ]