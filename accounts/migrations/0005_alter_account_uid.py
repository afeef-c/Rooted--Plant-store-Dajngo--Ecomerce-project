# Generated by Django 5.0.1 on 2024-02-15 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x00000144E38A1C60>', max_length=200),
        ),
    ]
