# Generated by Django 4.1.3 on 2022-12-31 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('bio', models.TextField(default='no bio...')),
                ('country', models.CharField(max_length=50)),
                ('avatar', models.ImageField(default='avatar.jpg', upload_to='profile_images')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
