# Generated by Django 4.2.5 on 2024-07-16 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('untersetzerBroker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='coaster',
        ),
    ]