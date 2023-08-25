# Generated by Django 4.2.4 on 2023-08-24 11:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_deal_date_of_order_alter_deal_date_of_shipment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('smartup_id', models.CharField(max_length=255)),
                ('assigned_users', models.ManyToManyField(blank=True, related_name='workplaces', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]