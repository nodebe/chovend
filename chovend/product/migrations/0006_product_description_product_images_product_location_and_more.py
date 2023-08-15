# Generated by Django 4.2.3 on 2023-08-01 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_socialmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.CharField(default='[]', max_length=1000),
        ),
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.city'),
        ),
        migrations.AddField(
            model_name='product',
            name='search_description',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.CreateModel(
            name='ProductSocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('social_media', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.socialmedia')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='social_media_urls',
            field=models.ManyToManyField(through='product.ProductSocialMedia', to='product.socialmedia'),
        ),
    ]