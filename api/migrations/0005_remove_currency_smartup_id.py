# Generated by Django 4.2.4 on 2023-08-09 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_paymenttype_currency_alter_orderdetails_deal_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="currency",
            name="smartup_id",
        ),
    ]
