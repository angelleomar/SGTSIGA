# Generated by Django 4.0.8 on 2023-06-23 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_courseoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='year',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7'), (4, '8'), (4, '9')], default=0),
        ),
    ]
