# Generated by Django 4.2.16 on 2024-10-31 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_post_media_alter_post_published_at_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(default='Tech and Gadgets', related_name='posts', to='blog.category'),
        ),
    ]
