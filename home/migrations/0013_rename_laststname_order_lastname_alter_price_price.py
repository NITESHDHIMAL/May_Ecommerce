# Generated by Django 4.0.4 on 2022-05-21 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_price_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='laststname',
            new_name='lastname',
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.CharField(choices=[('10 To 100', '10 To 100'), ('10000 To 20000', '10000 To 20000'), ('100 To 1000', '100 To 1000'), ('1000 To 10000', '1000 To 10000')], max_length=100),
        ),
    ]
