# Generated by Django 4.0.3 on 2022-03-20 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CuSell', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=20, verbose_name='Password'),
        ),
    ]