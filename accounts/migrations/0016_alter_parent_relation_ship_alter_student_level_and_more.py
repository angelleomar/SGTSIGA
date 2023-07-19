# Generated by Django 4.0.8 on 2023-07-16 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='relation_ship',
            field=models.TextField(blank=True, choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Hermano', 'Hermano'), ('Hermana', 'Hermana'), ('Abuela', 'Abuela'), ('Abuelo', 'Abuelo'), ('Otro', 'Otro')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(choices=[('Licenciatura', 'Licenciatura'), ('Maestría', 'Maestría')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='default.png', null=True, upload_to='profile_pictures/%Y/%m/%d/'),
        ),
    ]
