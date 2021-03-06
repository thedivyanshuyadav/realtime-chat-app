# Generated by Django 3.2.6 on 2021-08-23 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=5000)),
                ('datetime', models.DateTimeField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver_requests_created', to='chat_system.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender_requests_created', to='chat_system.user')),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
    ]
