# Generated by Django 4.2.5 on 2023-10-17 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_delete_customtokenblacklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_password_rest',
        ),
        migrations.AddField(
            model_name='user',
            name='is_password_reset',
            field=models.BooleanField(default=True),
        ),
    ]
