# Generated by Django 4.0.6 on 2024-01-14 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20231230_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.CharField(default='Unnamed device: None', max_length=50),
        ),
    ]
