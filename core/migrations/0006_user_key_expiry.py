# Generated by Django 4.2.5 on 2023-10-17 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_forget_password_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='key_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]