# Generated by Django 4.0.3 on 2022-04-05 11:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_alter_solvedtest_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='solvedtest',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 14, 16, 12, 21777)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solvedtest',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 14, 16, 18, 112540)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solvedtest',
            name='right_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='SolvedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tests.question')),
            ],
        ),
        migrations.AddField(
            model_name='solvedtest',
            name='answers',
            field=models.ManyToManyField(to='tests.solvedquestion'),
        ),
    ]
