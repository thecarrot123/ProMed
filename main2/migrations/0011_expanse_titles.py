# Generated by Django 3.2.5 on 2022-03-27 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main2', '0010_alharamtransfer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='expanse',
            name='titles',
            field=models.CharField(default='asd', max_length=50),
        ),
    ]