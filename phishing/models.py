from django.db import models

# Create your models here.

class MTurkUser(models.Model):
    workerId = models.CharField(max_length=30, primary_key=True)

class Constraint(models.Model):
    data_type = models.CharField(max_length=100, primary_key=True)
    data = models.TextField()

class Submission(models.Model):
    creator = models.ForeignKey(MTurkUser, models.SET_NULL, null=True)
    assignmentId = models.CharField(max_length=100, primary_key=True)
    when_submitted = models.DateTimeField(auto_now_add=True) 
    payout = models.BooleanField()
    text = models.TextField()
    constraints = models.ManyToManyField(Constraint)

class Rating(models.Model):
    creator = models.ForeignKey(MTurkUser, models.SET_NULL, null=True)
    assignmentId = models.CharField(max_length=100, primary_key=True)
    when_submitted = models.DateTimeField(auto_now_add=True)
    submission = models.ForeignKey(Submission, models.CASCADE)
