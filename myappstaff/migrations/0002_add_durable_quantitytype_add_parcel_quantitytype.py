# Generated by Django 4.1.3 on 2023-01-07 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappstaff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_durable',
            name='quantitytype',
            field=models.CharField(choices=[('ต้องการระบุจำนวน', 'ต้องการระบุจำนวน'), ('∞', '∞')], default='ต้องการระบุจำนวน', max_length=200),
        ),
        migrations.AddField(
            model_name='add_parcel',
            name='quantitytype',
            field=models.CharField(choices=[('ต้องการระบุจำนวน', 'ต้องการระบุจำนวน'), ('∞', '∞')], default='ต้องการระบุจำนวน', max_length=200),
        ),
    ]
