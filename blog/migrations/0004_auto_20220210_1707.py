# Generated by Django 3.2.11 on 2022-02-10 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20220210_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecolumn',
            options={'ordering': ('-created_time',), 'verbose_name': '博客栏目', 'verbose_name_plural': '博客栏目'},
        ),
        migrations.AddField(
            model_name='articlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='articles/%Y%m%d/'),
        ),
    ]
