# Generated by Django 4.2.5 on 2023-10-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_key_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_password_rest',
            field=models.BooleanField(default=True),
        ),
    ]
