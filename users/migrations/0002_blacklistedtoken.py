# Generated by Django 5.1.5 on 2025-01-29 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=500, unique=True)),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'blacklisted_tokens',
                'ordering': ['-created_at'],
            },
        ),
    ]
