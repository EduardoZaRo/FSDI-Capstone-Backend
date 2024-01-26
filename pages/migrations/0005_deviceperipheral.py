# Generated by Django 4.0.6 on 2024-01-18 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_device_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevicePeripheral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.device')),
                ('peripheral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.peripheral')),
            ],
        ),
    ]