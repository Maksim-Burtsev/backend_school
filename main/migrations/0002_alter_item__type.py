# Generated by Django 4.0.5 on 2022-06-17 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='_type',
            field=models.CharField(choices=[('offer', 'OFFER'), ('category', 'CATEGORY')], max_length=21),
        ),
    ]