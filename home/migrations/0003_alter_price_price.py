# Generated by Django 4.0.4 on 2022-05-19 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_color_color_for_alter_price_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.CharField(choices=[('1000 To 10000', '1000 To 10000'), ('10 To 100', '10 To 100'), ('100 To 1000', '100 To 1000'), ('10000 To 20000', '10000 To 20000')], max_length=100),
        ),
    ]
