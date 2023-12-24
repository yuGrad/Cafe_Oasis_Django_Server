# Generated by Django 3.2 on 2023-12-24 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CafeRating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('rating_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'CafeRating',
            },
        ),
        migrations.CreateModel(
            name='VisitHistory',
            fields=[
                ('visit_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_spend', models.DecimalField(decimal_places=0, max_digits=10)),
                ('visit_date', models.DateTimeField()),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cafe.cafe')),
            ],
            options={
                'db_table': 'VisitHistory',
            },
        ),
    ]
