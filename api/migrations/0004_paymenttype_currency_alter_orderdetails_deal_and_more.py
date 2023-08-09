# Generated by Django 4.2.4 on 2023-08-09 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_city_smartup_id_district_smartup_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttype',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.currency'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.deal'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='api.product'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='api.user'),
        ),
    ]
