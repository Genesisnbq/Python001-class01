# Generated by Django 2.2.13 on 2020-07-30 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('content', models.CharField(max_length=400)),
                ('date', models.DateField()),
            ],
        ),
    ]
