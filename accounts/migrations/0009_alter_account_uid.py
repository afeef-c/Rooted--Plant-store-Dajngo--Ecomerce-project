# Generated by Django 5.0.1 on 2024-02-22 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_account_uid_wallet_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000023E2DE14900>', max_length=200),
        ),
    ]