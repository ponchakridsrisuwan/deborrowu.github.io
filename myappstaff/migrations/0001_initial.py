# Generated by Django 4.1.3 on 2023-01-07 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_CategoryStatus', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_CategoryType', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SettingPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameposition', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Add_Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('nametype', models.CharField(choices=[('วัสดุ', 'วัสดุ'), ('ครุภัณฑ์', 'ครุภัณฑ์')], default='วัสดุ', max_length=200)),
                ('statustype', models.CharField(choices=[('ต้องคืน', 'ต้องคืน'), ('ไม่ต้องคืน', 'ไม่ต้องคืน')], default='ไม่ต้องคืน', max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('image', models.ImageField(upload_to='Parcel')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('borrow_count', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='category_parcel', to='myappstaff.categorytype')),
                ('nameposition', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='position_parcel', to='myappstaff.settingposition')),
                ('status', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='status_parcel', to='myappstaff.categorystatus')),
            ],
        ),
        migrations.CreateModel(
            name='Add_Durable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='', max_length=12)),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('nametype', models.CharField(choices=[('วัสดุ', 'วัสดุ'), ('ครุภัณฑ์', 'ครุภัณฑ์')], default='ครุภัณฑ์', max_length=200)),
                ('statustype', models.CharField(choices=[('ต้องคืน', 'ต้องคืน'), ('ไม่ต้องคืน', 'ไม่ต้องคืน')], default='ต้องคืน', max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('numdate', models.PositiveIntegerField(default=1)),
                ('description', models.TextField(blank=True, default='')),
                ('image', models.ImageField(upload_to='Durable')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('borrow_count', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='category_durable', to='myappstaff.categorytype')),
                ('nameposition', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='position_durable', to='myappstaff.settingposition')),
                ('status', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='status_durable', to='myappstaff.categorystatus')),
            ],
        ),
    ]
