# Generated by Django 3.2.12 on 2022-02-22 08:35

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20220210_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='can_comment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='body',
            field=mdeditor.fields.MDTextField(),
        ),
    ]