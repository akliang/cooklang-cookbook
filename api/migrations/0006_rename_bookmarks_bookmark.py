# Generated by Django 3.2.13 on 2022-04-23 17:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_bookmarks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bookmarks',
            new_name='Bookmark',
        ),
    ]
