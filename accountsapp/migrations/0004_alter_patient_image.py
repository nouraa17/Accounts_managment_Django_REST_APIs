# Generated by Django 4.1.7 on 2023-04-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsapp', '0003_alter_patient_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(upload_to='patient_images'),
        ),
    ]
