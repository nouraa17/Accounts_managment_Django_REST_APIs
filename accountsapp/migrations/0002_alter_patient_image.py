# Generated by Django 4.1.7 on 2023-04-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]
