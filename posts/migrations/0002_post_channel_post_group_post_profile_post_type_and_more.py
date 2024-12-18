# Generated by Django 5.0.7 on 2024-08-26 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_alter_viewer_unique_together'),
        ('posts', '0001_initial'),
        ('profiles', '0002_alter_profile_banner_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channel_posts', to='groups.channel'),
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_posts', to='groups.group'),
        ),
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_posts', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('profile', 'Profile'), ('group', 'Group'), ('channel', 'Channel')], default='profile', max_length=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='posts_media'),
        ),
        migrations.AlterField(
            model_name='repost',
            name='text',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
