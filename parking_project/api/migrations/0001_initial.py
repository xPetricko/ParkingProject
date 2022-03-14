# Generated by Django 3.2.9 on 2022-03-14 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_pos', models.PositiveIntegerField()),
                ('y_pos', models.PositiveIntegerField()),
                ('x_width', models.PositiveIntegerField()),
                ('y_width', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('total_spaces', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_number', models.CharField(max_length=25)),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkinglot')),
            ],
        ),
        migrations.CreateModel(
            name='SpaceOccupationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('occupied', models.BooleanField()),
                ('parking_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkingspace')),
            ],
        ),
        migrations.CreateModel(
            name='NetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=250)),
                ('trained', models.BooleanField()),
                ('trained_date', models.DateField()),
                ('parkingLot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.parkinglot')),
            ],
        ),
        migrations.CreateModel(
            name='LotOccupationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('occupied', models.BooleanField()),
                ('parkingLot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.parkinglot')),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_number', models.PositiveIntegerField()),
                ('resolution_x', models.PositiveIntegerField()),
                ('resolution_y', models.PositiveIntegerField()),
                ('parkingLot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkinglot')),
                ('parking_space', models.ManyToManyField(through='api.BoundingBox', to='api.ParkingSpace')),
            ],
        ),
        migrations.AddField(
            model_name='boundingbox',
            name='camera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.camera'),
        ),
        migrations.AddField(
            model_name='boundingbox',
            name='parking_space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkingspace'),
        ),
    ]
