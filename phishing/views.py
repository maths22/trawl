import datetime

import boto3
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.clickjacking import xframe_options_exempt

from phishing.forms import CreateTemplate
from phishing.models import Submission, MTurkUser, Rating

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

create_hits_in_live = False

environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
            "preview": "https://www.mturk.com/mturk/preview",
            "manage": "https://requester.mturk.com/mturk/manageHITs",
            "reward": "0.00"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
            "preview": "https://workersandbox.mturk.com/mturk/preview",
            "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
            "reward": "0.11"
        },
}
mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

session = boto3.Session()
client = session.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=mturk_environment['endpoint'],
)


def index(request):
    template = loader.get_template('phishing/index.html')
    context = {
        'testing': 'hi there',
    }
    return HttpResponse(template.render(context, request))


@xframe_options_exempt
def submit(request):
    template = loader.get_template('phishing/submit.html')
    context = {
        'directions': """
        Your target is Roger Johnson, a student employee at the University of Oak Creek.
	    Your message must be written as if sent by Thomas Smith, an HR employee at the University.
	    Your goal is to convince Roger to send ``Thomas'' his bank account information.
	
        The personal information you may include about Roger includes the following:
        <dl>
            <dt>Name</dt> <dd>Roger Johnson</dd>
            <dt>Date of Birth</dt> <dd>April 18, 1995</dd>
            <dt>Supervisior</dt> <dd>Alice Davis</dd>
            <dt>Position</dt> <dd>Math Grader</dd>
        </dl>
        """,
        'worker_id': request.GET.get('workerId', ''),
        'assignment_id': request.GET.get('assignmentId', ''),
        'turk_submit_to': request.GET.get('turkSubmitTo', '')
    }
    return HttpResponse(template.render(context, request))


def submit_template(request):
    tmpl = CreateTemplate({
        'worker_id': request.POST.get('worker_id', ''),
        'assignment_id':  request.POST.get('assignmentId', ''),
        'subject': request.POST.get('message_subject', ''),
        'message_template': request.POST.get('message_template', '')
    })
    if tmpl.is_valid():
        tmpl.execute()
    else:
        return JsonResponse({'result': False})

    return JsonResponse({'result': True})


@xframe_options_exempt
def review(request):
    template = loader.get_template('phishing/review.html')
    task_id = request.GET.get('task', '')
    objs = Submission.objects.filter(task=task_id).all()

    context = {
        'name': 'John Doe',
        'worker_id': request.GET.get('workerId', ''),
        'assignment_id': request.GET.get('assignmentId', ''),
        'turk_submit_to': request.GET.get('turkSubmitTo', ''),
        'task': request.GET.get('task', ''),
        'messages': list(map(lambda x: {
                    'from': 'John Doe <john@example.com>',
                    'subject': x.subject,
                    'body': x.text
                }, objs))
    }
    return HttpResponse(template.render(context, request))


def submit_review(request):
    logger.warning(request.POST)
    worker_id = request.POST.get('worker_id', '')
    task_id = request.POST.get('task', '')
    assignment_id = request.POST.get('assignmentId', '')
    results = request.POST.get('results', '').split(",")

    try:
        mt_usr = MTurkUser.objects.get(pk=worker_id)
    except MTurkUser.DoesNotExist:
        mt_usr = MTurkUser(workerId=worker_id)
        mt_usr.save()

    submissions = Submission.objects.filter(task=task_id).all()
    for (submission, result) in zip(submissions, results):
        rating = Rating(
            creator=mt_usr,
            assignmentId=assignment_id,
            when_submitted=datetime.datetime.now(),
            submission=submission,
            is_spam=result == 'spam',
            is_email=True,
            is_comprehensible=True,
            is_correct_info=True,
        )
        rating.save()

        if not submission.payout:
            all_ratings = Rating.objects.filter(assignmentId=assignment_id).all()
            if len(all_ratings) < 10:
                continue
            client.approve_assignment(
                AssignmentId=submission.assignmentId
            )
            spam_count = map(lambda x: x.is_spam, all_ratings).count(True)
            if spam_count <= 1:
                client.send_bonus(
                    WorkerId=submission.creator.workerId,
                    AssignmentId=submission.assignmentId,
                    BonusAmount=0.5, #TODO set the bonus amount
                    Reason="Your submission was almost universally seen as not spam"
                )
            submission.payout = True
            submission.save()

    return JsonResponse({'result': True})