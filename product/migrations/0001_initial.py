# Generated by Django 2.1.2 on 2018-10-05 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('price', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('description', models.TextField(max_length=300, verbose_name='商品描述')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='ProductImags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('pictures1', models.ImageField(upload_to='static/ProductImages/%Y/%m/%d')),
                ('pictures2', models.ImageField(null=True, upload_to='static/ProductImages/%Y/%m/%d')),
                ('pictures3', models.ImageField(null=True, upload_to='static/ProductImages/%Y/%m/%d')),
                ('pictures4', models.ImageField(null=True, upload_to='static/ProductImages/%Y/%m/%d')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'ordering': ['-c_time'],
            },
        ),
    ]