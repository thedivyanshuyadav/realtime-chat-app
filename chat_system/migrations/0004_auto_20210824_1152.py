# Generated by Django 3.2.6 on 2021-08-24 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_system', '0003_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_contact_requests_created', to='chat_system.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_user_requests_created', to='chat_system.user')),
            ],
            options={
                'ordering': ['contact'],
            },
        ),
    ]
