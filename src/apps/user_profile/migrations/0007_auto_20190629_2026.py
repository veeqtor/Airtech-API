# Generated by Django 2.2.2 on 2019-06-29 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20190629_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='passport_photo_url',
            new_name='photo_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='photo_public_id',
            field=models.CharField(default='iowjgoirgoierhgio934843897986798',
                                   max_length=100,
                                   verbose_name='Passport public id'),
        ),
    ]
