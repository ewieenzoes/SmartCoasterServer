# Generated by Django 4.2.5 on 2024-07-16 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('edition', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BeverageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('edition', models.CharField(max_length=200)),
                ('weight', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_reference', models.CharField(max_length=200)),
                ('total_price', models.FloatField(default=0)),
                ('tip', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FoodTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Untersetzer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=5)),
                ('glass_level', models.IntegerField(default=0)),
                ('timeout', models.BooleanField()),
                ('description', models.CharField(max_length=200)),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table', to='untersetzerBroker.table')),
            ],
        ),
        migrations.CreateModel(
            name='tempCoasterGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coasters', models.ManyToManyField(to='untersetzerBroker.untersetzer')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table_for_tempgroup', to='untersetzerBroker.table')),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='coasters',
            field=models.ManyToManyField(related_name='coasterForTable', to='untersetzerBroker.untersetzer'),
        ),
        migrations.CreateModel(
            name='serviceCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serviceCall', to='untersetzerBroker.untersetzer')),
            ],
        ),
        migrations.CreateModel(
            name='QuickAccessTemplateFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='untersetzerBroker.foodtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='QuickAccessTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beverage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='untersetzerBroker.beveragetemplate')),
            ],
        ),
        migrations.CreateModel(
            name='paymentSuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentSuccess', to='untersetzerBroker.untersetzer')),
            ],
        ),
        migrations.CreateModel(
            name='paymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
                ('coaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='untersetzerBroker.untersetzer')),
            ],
        ),
        migrations.CreateModel(
            name='lastBeverages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beverages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_beverage', to='untersetzerBroker.beverage')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('coaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='untersetzerBroker.untersetzer')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutPositions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_reference', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('name', models.CharField(max_length=200)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='untersetzerBroker.checkout')),
            ],
        ),
        migrations.AddField(
            model_name='checkout',
            name='coaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='untersetzerBroker.untersetzer'),
        ),
        migrations.AddField(
            model_name='beverage',
            name='coaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beverage', to='untersetzerBroker.untersetzer'),
        ),
    ]
