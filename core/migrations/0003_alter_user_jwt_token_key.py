# Generated by Django 4.2.5 on 2023-10-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_jwt_token_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='jwt_token_key',
            field=models.CharField(max_length=12),
        ),
    ]
