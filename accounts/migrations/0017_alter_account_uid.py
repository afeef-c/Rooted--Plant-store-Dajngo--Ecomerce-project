# Generated by Django 5.0.1 on 2024-03-04 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_account_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001D1263FDB20>', max_length=200),
        ),
    ]
