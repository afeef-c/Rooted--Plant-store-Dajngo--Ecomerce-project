# Generated by Django 5.0.1 on 2024-01-25 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001505CF1FEC0>', max_length=200),
        ),
    ]