# Generated by Django 2.0.7 on 2019-09-19 13:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0010_auto_20190919_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('date_start', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('date_end', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=20)),
                ('contract_file', models.FileField(upload_to='contracts/')),
                ('add_date', models.DateTimeField(default=datetime.datetime.now)),
                ('planned_invoices', models.CharField(blank=True, max_length=200)),
                ('account', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Account')),
            ],
        ),
    ]
