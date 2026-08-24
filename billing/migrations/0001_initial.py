from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, default='', max_length=20)),
                ('cloth_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stitching_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shirt_ready', models.BooleanField(default=False)),
                ('pant_ready', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt_length', models.CharField(blank=True, default='', max_length=20)),
                ('shirt_chest', models.CharField(blank=True, default='', max_length=20)),
                ('shirt_stomach', models.CharField(blank=True, default='', max_length=20)),
                ('shirt_sleeve', models.CharField(blank=True, default='', max_length=20)),
                ('shirt_shoulder', models.CharField(blank=True, default='', max_length=20)),
                ('shirt_collar', models.CharField(blank=True, default='', max_length=20)),
                ('pant_length', models.CharField(blank=True, default='', max_length=20)),
                ('pant_waist', models.CharField(blank=True, default='', max_length=20)),
                ('pant_thigh', models.CharField(blank=True, default='', max_length=20)),
                ('pant_bottom', models.CharField(blank=True, default='', max_length=20)),
                ('pant_hip', models.CharField(blank=True, default='', max_length=20)),
                ('pant_seat_langot', models.CharField(blank=True, default='', max_length=20)),
                ('notes', models.TextField(blank=True, default='')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bill', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='measurement', to='billing.bill')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together={('owner', 'bill_no')},
        ),
    ]
