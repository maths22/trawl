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
                'subject': 'Metra Alert - Pre-Memorial Day Early Getaway Service - Friday, May 25',
                'from': 'Metra <servicealerts@metramail.com>',
                'body': """
                Metra Alert - Pre-Memorial Day Early Getaway Service - Friday, May
25

Metra will operate a Pre-Memorial Day Early Getaway scehdule on Friday, May 25.  As a reminder,
a Sunday/Holiday schedule will be in effect on Memorial Day (Monday, May
28). For a summary of the service changes, please click here.

                       *This email was sent to: john@sample.com* 

 This email was sent by: Metra
 547 W. Jackson Boulevard
 Chicago, IL 60661-5717 USA 

 We respect your right to privacy - view our policy
 Unsubscribe
if you no longer want to receive Metra Alert Email Notifications.
 Please do not reply to this email as it was generated by an automated
system.
 If you have questions or comments, you may contact us at
"""
            },
            {
                'subject': 'John, Is Your Arrest Record Online? Check Now!!',
                'from': 'SpyFly <zGIJ57yDik2r7136hd3@neofdjrr6r945lcjk3.lottery.realitiesconsultancy.com>',
                'body': """
                <CenTer><h1><a Href="#"><FoNT Face="Bodoni MT Black" Color=#0750E1 Size=5 >Introducing Public Records Online</br></br>
<br///><a href="#" style="font: 28px Agency FB, serif; 
    display: block;
    text-decoration: none;
    width: 350px;
    height: 35px;
    background: #FE9A2E;
    padding: 10px;
    text-align: center;
    border-radius: 1px;
    color:#FFFFFF;
    font-weight: bold;" target="_blank"> Click HERE ➡ <br///>
<br///><a href="#"><img src="https://i.imgur.com/JnTdGIr.png"></a><br///>
<a href="#"><img src="https://i.imgur.com/vOIz9H4.png"></a><br///>
 <a Href="#">
 <Br><IMg src="http://i.imgur.com/zVmEFrh.jpg"><Br></a>
                """
            },
            {
                'subject': 'Urgent: Open now',
                'from': 'ssmith@example.com',
                'body': """
                Please send me all your bank account numbers ASAP.
                """
            },
            {
                'subject': 'W2 Forms',
                'from': 'CEO <ceo@company.com>',
                'body': """
                Hi John,
                
                Test...
                """
            }
        ]
    }
    return HttpResponse(template.render(context, request))