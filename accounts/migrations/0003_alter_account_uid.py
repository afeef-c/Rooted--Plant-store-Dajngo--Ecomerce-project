# Generated by Django 5.0.1 on 2024-01-21 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_otp_account_uid_alter_account_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000002232141FEC0>', max_length=200),
        ),
    ]
