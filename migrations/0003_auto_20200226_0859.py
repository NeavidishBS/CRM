# Generated by Django 2.0.7 on 2020-02-26 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_contract_contract_add_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_file',
            field=models.FileField(blank=True, upload_to='contracts/'),
        ),
    ]
