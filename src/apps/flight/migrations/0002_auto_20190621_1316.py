# Generated by Django 2.2.2 on 2019-06-21 13:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('deleted', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('updated_by', models.CharField(blank=True, max_length=200)),
                ('type',
                 models.CharField(choices=[('ECO', 'Economy class'),
                                           ('BUS', 'Business class')],
                                  max_length=20,
                                  verbose_name='Seat type')),
                ('booked',
                 models.BooleanField(default=False, verbose_name='Is booked')),
                ('reserved',
                 models.BooleanField(default=False,
                                     verbose_name='Is reserved')),
                ('number',
                 models.CharField(max_length=10, verbose_name='Seat number')),
            ],
            options={
                'verbose_name_plural': 'Plane seats',
                'db_table': 'fl_seats',
            },
        ),
        migrations.RemoveField(
            model_name='plane',
            name='seats',
        ),
        migrations.AddField(
            model_name='plane',
            name='seats',
            field=models.ManyToManyField(related_name='plane',
                                         to='flight.Seats'),
        ),
    ]