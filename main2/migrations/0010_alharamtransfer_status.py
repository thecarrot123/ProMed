# Generated by Django 3.2.5 on 2022-03-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main2', '0009_auto_20220327_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='alharamtransfer',
            name='status',
            field=models.CharField(choices=[('C', 'Confirmed'), ('U', 'Unconfirmed')], default='U', max_length=1),
        ),
    ]
