# Generated by Django 3.2.4 on 2022-04-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paymenttype_mobile_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenttype',
            name='mobile_Number',
        ),
        migrations.RemoveField(
            model_name='paymenttype',
            name='payType',
        ),
        migrations.RemoveField(
            model_name='paymenttype',
            name='user',
        ),
        migrations.AddField(
            model_name='paymenttype',
            name='bill_paid',
            field=models.BooleanField(default=False),
        ),
    ]