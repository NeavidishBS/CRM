# Generated by Django 2.0.7 on 2020-03-04 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0004_auto_20200226_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('contract_id', models.IntegerField(default=0)),
                ('field_name', models.CharField(blank=True, max_length=200)),
                ('old_value', models.CharField(blank=True, max_length=200)),
                ('new_value', models.CharField(blank=True, max_length=200)),
                ('ip', models.GenericIPAddressField()),
                ('changed_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]