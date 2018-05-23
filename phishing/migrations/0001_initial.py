# Generated by Django 2.0.5 on 2018-05-23 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constraint',
            fields=[
                ('data_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MTurkUser',
            fields=[
                ('workerId', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('assignmentId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('when_submitted', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='phishing.MTurkUser')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('assignmentId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('when_submitted', models.DateTimeField(auto_now_add=True)),
                ('payout', models.BooleanField()),
                ('text', models.TextField()),
                ('constraints', models.ManyToManyField(to='phishing.Constraint')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='phishing.MTurkUser')),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phishing.Submission'),
        ),
    ]