# Generated by Django 5.0.1 on 2024-01-27 06:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_account_otp_remove_account_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]