# Generated by Django 4.2.5 on 2023-09-23 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='detail_answer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
