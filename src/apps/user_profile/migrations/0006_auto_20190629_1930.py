# Generated by Django 2.2.2 on 2019-06-29 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_userprofile_passport_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='passport_photo',
            new_name='passport_photo_url',
        ),
    ]
