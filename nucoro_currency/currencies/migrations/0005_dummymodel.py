# Generated by Django 3.1.11 on 2021-05-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0004_provider_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Exchange Rate Evolution',
                'managed': False,
            },
        ),
    ]
