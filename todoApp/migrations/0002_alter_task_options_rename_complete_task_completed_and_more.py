# Generated by Django 4.1 on 2022-08-26 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['date']},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='complete',
            new_name='completed',
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('entertainment', 'Entertainment'), ('fitness', 'Fitness'), ('others', 'Others')], default='others', max_length=20),
        )
    ]
