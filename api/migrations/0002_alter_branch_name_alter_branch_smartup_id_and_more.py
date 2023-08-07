# Generated by Django 4.2.4 on 2023-08-07 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='branch',
            name='smartup_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AlterField(
            model_name='deal',
            name='smartup_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='total',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='smartup_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='smartup_id',
            field=models.CharField(max_length=255),
        ),
    ]