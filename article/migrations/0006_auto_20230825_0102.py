# Generated by Django 3.2 on 2023-08-24 17:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20230824_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ImageField(upload_to='avatar/%Y%m%d')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 17, 2, 32, 628399, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 24, 17, 2, 32, 627843, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='article',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='article.avatar'),
        ),
    ]
