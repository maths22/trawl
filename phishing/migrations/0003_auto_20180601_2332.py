# Generated by Django 2.0.5 on 2018-06-01 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phishing', '0002_add_question_responses'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hit_id', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='subject',
            field=models.TextField(default='Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='phishing.EvaluationTask'),
        ),
    ]
