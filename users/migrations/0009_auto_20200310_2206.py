# Generated by Django 2.2.5 on 2020-03-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200304_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.CharField(default=0, max_length=10, null=True),
        ),
    ]
