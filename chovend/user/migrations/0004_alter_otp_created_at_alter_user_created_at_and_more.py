# Generated by Django 4.2.3 on 2023-07-23 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 10, 0, 49, 406415)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 10, 0, 49, 405737)),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 10, 0, 49, 405754)),
        ),
    ]