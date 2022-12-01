# Generated by Django 2.2.16 on 2022-08-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220819_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='title',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, related_name='titles', to='reviews.Genre', verbose_name='title related genre'),
        ),
    ]
