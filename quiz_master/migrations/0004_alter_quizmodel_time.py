# Generated by Django 4.2.4 on 2023-08-22 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_master', '0003_quizmodel_quiz_desc_quizmodel_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='time',
            field=models.IntegerField(default='1', help_text='Duration of the quiz in seconds'),
        ),
    ]
