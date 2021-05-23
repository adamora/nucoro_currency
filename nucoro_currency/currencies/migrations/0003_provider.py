# Generated by Django 3.1.11 on 2021-05-23 13:00

from django.db import migrations, models
import nucoro_currency.currencies.validators


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Provider name', max_length=20)),
                ('slug', models.SlugField(help_text='Unique slug identifier for a provider', unique=True)),
                ('path', models.CharField(help_text='Path to a provider adapter class', max_length=250, validators=[nucoro_currency.currencies.validators.validate_provider_path])),
                ('default', models.BooleanField(default=False, help_text='Provider priority')),
            ],
        ),
    ]
