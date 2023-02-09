# Generated by Django 4.1.3 on 2023-02-08 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookprog', '0003_alter_progress_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progress',
            old_name='completed',
            new_name='active',
        ),
        migrations.RemoveField(
            model_name='book',
            name='active',
        ),
        migrations.AddField(
            model_name='book',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='progress',
            name='progress_id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]