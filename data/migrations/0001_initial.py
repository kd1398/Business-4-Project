# Generated by Django 4.2.5 on 2023-11-29 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('data', models.JSONField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.category')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileDataHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('data', models.JSONField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('original_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.filedata')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='filedata',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.module'),
        ),
        migrations.AddField(
            model_name='filedata',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]