# Generated by Django 4.2.16 on 2024-11-14 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AttributeName', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'products_attribute',
            },
        ),
        migrations.CreateModel(
            name='AttributeValues',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AttributeValue', models.CharField(max_length=255)),
                ('Attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='inventory.attributes')),
            ],
            options={
                'db_table': 'products_attribute_value',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ProductID', models.BigIntegerField(unique=True)),
                ('ProductCode', models.CharField(max_length=255, unique=True)),
                ('ProductName', models.CharField(max_length=255)),
                ('ProductImage', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='uploads/')),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
                ('UpdatedDate', models.DateTimeField(blank=True, null=True)),
                ('IsFavourite', models.BooleanField(default=False)),
                ('Active', models.BooleanField(default=True)),
                ('HSNCode', models.CharField(blank=True, max_length=255, null=True)),
                ('TotalStock', models.DecimalField(blank=True, decimal_places=8, default=0.0, max_digits=20, null=True)),
                ('CreatedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'products_product',
                'ordering': ('-CreatedDate', 'ProductID'),
                'unique_together': {('ProductCode', 'ProductID')},
            },
        ),
        migrations.CreateModel(
            name='ProductsVariation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('DisplayName', models.CharField(max_length=255)),
                ('ProductCode', models.CharField(max_length=255)),
                ('ProductImage', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='uploads/variations/')),
                ('TotalStock', models.DecimalField(decimal_places=8, default=0.0, max_digits=20)),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
                ('UpdatedDate', models.DateTimeField(blank=True, null=True)),
                ('IsDeleted', models.BooleanField(default=False)),
                ('IsActive', models.BooleanField(default=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='inventory.products')),
            ],
            options={
                'db_table': 'products_variation',
                'ordering': ('-CreatedDate',),
            },
        ),
        migrations.CreateModel(
            name='VariationAttributes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('AttributeValue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='inventory.attributevalues')),
                ('Variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='inventory.productsvariation')),
            ],
            options={
                'db_table': 'products_variation_attribute',
            },
        ),
    ]
