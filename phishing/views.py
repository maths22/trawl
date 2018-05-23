from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('phishing/index.html')
    context = {
        'testing': 'hi there',
    }
    return HttpResponse(template.render(context, request))


def submit_template(request):
    template = loader.get_template('phishing/submit.html')
    context = {
        'directions': 'TODO',
    }
    return HttpResponse(template.render(context, request))
