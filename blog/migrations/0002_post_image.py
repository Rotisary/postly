# Generated by Django 4.2.4 on 2023-08-25 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default_user_profile.jpg', upload_to='user_profile_pics'),
        ),
    ]
