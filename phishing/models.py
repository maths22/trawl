from django.db import models


class MTurkUser(models.Model):
    workerId = models.CharField(max_length=30, primary_key=True)


class Constraint(models.Model):
    data_type = models.CharField(max_length=100, primary_key=True)
    data = models.TextField()


class EvaluationTask(models.Model):
    id = models.AutoField(primary_key=True)
    hit_id = models.CharField(max_length=100, null=True)


class Submission(models.Model):
    creator = models.ForeignKey(MTurkUser, models.SET_NULL, null=True)
    task = models.ForeignKey(EvaluationTask, models.SET_NULL, null=True)
    assignmentId = models.CharField(max_length=100, primary_key=True)
    when_submitted = models.DateTimeField(auto_now_add=True)
    payout = models.BooleanField()
    subject = models.TextField()
    text = models.TextField()
    constraints = models.ManyToManyField(Constraint)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(MTurkUser, models.SET_NULL, null=True)
    assignmentId = models.CharField(max_length=100)
    when_submitted = models.DateTimeField(auto_now_add=True)
    submission = models.ForeignKey(Submission, models.CASCADE)
    is_spam = models.BooleanField()
    is_email = models.BooleanField()
    is_comprehensible = models.BooleanField()
    is_correct_info = models.BooleanField()
