# Generated by Django 4.2.4 on 2023-08-11 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_remove_currency_smartup_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="currency",
        ),
        migrations.AddField(
            model_name="payment",
            name="payment_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.paymenttype",
            ),
        ),
    ]
