# Generated by Django 2.2.2 on 2019-06-25 17:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '0006_auto_20190625_1523'),
        ('user', '0002_auto_20190619_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
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
                ('ticket_ref',
                 models.CharField(max_length=100,
                                  verbose_name='Ticket reference')),
                ('paid', models.BooleanField(default=False,
                                             verbose_name='Paid')),
                ('take_off',
                 models.CharField(max_length=100,
                                  null=True,
                                  verbose_name='Take off')),
                ('destination',
                 models.CharField(max_length=100,
                                  null=True,
                                  verbose_name='Destination')),
                ('seat_number',
                 models.CharField(max_length=100, verbose_name='Seat number')),
                ('type',
                 models.CharField(choices=[('ECO', 'Economy class'),
                                           ('BUS', 'Business class')],
                                  max_length=100,
                                  verbose_name='Type')),
                ('date', models.DateField(verbose_name='Date')),
                ('departure_time',
                 models.TimeField(verbose_name='Departure Time')),
                ('arrival_time',
                 models.TimeField(verbose_name='Arrival Time')),
                ('date_made',
                 models.DateTimeField(auto_now_add=True,
                                      verbose_name='Date made')),
                ('flight',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='ticket',
                                   to='flight.Flight')),
                ('made_by',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='ticket',
                                   to='user.User')),
            ],
            options={
                'verbose_name_plural': 'Tickets',
                'db_table': 'bo_tickets',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
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
                ('seat_number',
                 models.CharField(max_length=100, verbose_name='Seat number')),
                ('type',
                 models.CharField(choices=[('ECO', 'Economy class'),
                                           ('BUS', 'Business class')],
                                  max_length=20,
                                  verbose_name='Type')),
                ('date_made',
                 models.DateTimeField(auto_now_add=True,
                                      verbose_name='Date made')),
                ('flight',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='reservation',
                                   to='flight.Flight')),
                ('made_by',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='reservation',
                                   to='user.User')),
            ],
            options={
                'verbose_name_plural': 'Reservations',
                'db_table': 'bo_reservations',
            },
        ),
    ]
