# Generated by Django 4.0.3 on 2022-04-01 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.CharField(default='', max_length=10, primary_key=True, serialize=False, verbose_name='Image ID')),
            ],
            options={
                'db_table': 'Image',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('sid', models.CharField(default='', max_length=10, primary_key=True, serialize=False, verbose_name='User ID')),
                ('name', models.CharField(default='', max_length=10, verbose_name='Name')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='Email')),
                ('password', models.CharField(default='', max_length=20, verbose_name='Password')),
                ('introduction', models.TextField(default='', verbose_name='Personal introduction')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('portrait', models.ImageField(default='default/default.jpg', upload_to='portrait', verbose_name='User portrait')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('mid', models.AutoField(primary_key=True, serialize=False, verbose_name='Merchandise ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='Merchandise Name')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
                ('keyword', models.CharField(default='', max_length=15, verbose_name='Keyword')),
                ('description', models.TextField(default='', verbose_name='Description')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publish time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('image_1', models.ImageField(default='', upload_to='image', verbose_name='image_1')),
                ('image_2', models.ImageField(default='', upload_to='image', verbose_name='image_2')),
                ('image_3', models.ImageField(default='', upload_to='image', verbose_name='image_3')),
                ('image_4', models.ImageField(default='', upload_to='image', verbose_name='image_4')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CuSell.user')),
            ],
            options={
                'db_table': 'Merchandise',
            },
        ),
    ]
