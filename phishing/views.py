import datetime

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.clickjacking import xframe_options_exempt

from phishing.models import Submission, MTurkUser


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
        'directions': 'TODO',
        'worker_id': request.GET.get('workerId', ''),
        'assignment_id': request.GET.get('assignmentId', ''),
        'turk_submit_to': request.GET.get('turkSubmitTo', '')
    }
    return HttpResponse(template.render(context, request))


def submit_template(request):
    worker_id = request.POST.get('worker_id', '')
    assignment_id = request.POST.get('assignmentId', '')
    try:
        mt_usr = MTurkUser.objects.get(pk=worker_id)
    except MTurkUser.DoesNotExist:
        mt_usr = MTurkUser(workerId=worker_id)
        mt_usr.save()


    #todo validate
    s = Submission(assignmentId=assignment_id,
                   creator=mt_usr,
                   payout=False,
                   when_submitted=datetime.datetime.now(),
                   text=request.POST.get('message_template', ''))
    s.save()
    return JsonResponse({'result': 'success'})


@xframe_options_exempt
def review(request):
    template = loader.get_template('phishing/review.html')
    context = {
        'name': 'John Doe',
        'worker_id': request.GET.get('workerId', ''),
        'assignment_id': request.GET.get('assignmentId', ''),
        'turk_submit_to': request.GET.get('turkSubmitTo', ''),
        'messages': [
            {
                'subject': 'Subject 1',
                'from': 'Sample name <sample@example.com>',
                'body': 'Body'
            },
            {
                'subject': 'Subject 2',
                'from': 'Sample name <sample@example.com>',
                'body': 'Body2'
            }
        ]
    }
    return HttpResponse(template.render(context, request))