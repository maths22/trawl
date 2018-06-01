import datetime

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.clickjacking import xframe_options_exempt

from phishing.forms import CreateTemplate
from phishing.models import Submission, MTurkUser

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
        'messages': list(map(lambda x: {
                    'from': 'John Doe <john@example.com>',
                    'subject': x.subject,
                    'body': x.text
                }, objs))
    }
    return HttpResponse(template.render(context, request))