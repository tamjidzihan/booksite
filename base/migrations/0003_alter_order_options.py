# Generated by Django 4.2.5 on 2023-09-23 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can Cancel Order')]},
        ),
    ]
