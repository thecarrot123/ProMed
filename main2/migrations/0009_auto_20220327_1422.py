# Generated by Django 3.2.5 on 2022-03-27 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main2', '0008_rename_library_librarytransfer_library_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarytransfer',
            name='status',
            field=models.CharField(choices=[('C', 'Confirmed'), ('U', 'Unconfirmed')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='librarytransfer',
            name='library_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main2.library', verbose_name='المكتبة'),
        ),
        migrations.AlterField(
            model_name='librarytransfer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
    ]
