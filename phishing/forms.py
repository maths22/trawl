import datetime

import boto3
from django import forms

from .models import Submission, MTurkUser, EvaluationTask

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

class CreateTemplate(forms.Form):
    message_template = forms.CharField()
    subject = forms.CharField()
    worker_id = forms.CharField()
    assignment_id = forms.CharField()

    def execute(self):
        message_template = self.cleaned_data['message_template']
        subject = self.cleaned_data['subject']
        worker_id = self.cleaned_data['worker_id']
        assignment_id = self.cleaned_data['assignment_id']

        try:
            mt_usr = MTurkUser.objects.get(pk=worker_id)
        except MTurkUser.DoesNotExist:
            mt_usr = MTurkUser(workerId=worker_id)
            mt_usr.save()

        # todo validate
        s = Submission(assignmentId=assignment_id,
                       creator=mt_usr,
                       payout=False,
                       when_submitted=datetime.datetime.now(),
                       subject=subject,
                       text=message_template)
        s.save()

        objects = Submission.objects.filter(task__isnull=True)
        while len(objects) >= 3:
            targets = objects.all()[:3]
            et = EvaluationTask()
            et.save()
            for target in targets:
                target.task = et
                target.save()
            self.registerMturk(et)
            objects = Submission.objects.filter(task__isnull=True)


        return s

    def registerMturk(self, et):
        et_id = et.id

        url = "https://security.maths22.com/review?task=" + str(et_id)

        question = """
        <ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
          <ExternalURL>%s</ExternalURL>
          <FrameHeight>800</FrameHeight>
        </ExternalQuestion>
        """ % url

        # Create the HIT
        response = client.create_hit(
            MaxAssignments=10,
            LifetimeInSeconds=60000,
            AssignmentDurationInSeconds=6000,
            Reward=mturk_environment['reward'],
            Title='Mark emails as spam or not spam',
            Keywords='reading, classification',
            Description='Read some emails and decide if they are spam',
            Question=question,
            # QualificationRequirements=worker_requirements,
        )
        logger.warning(response)
        hit_id = response['HIT']['HITId']
        et.hit_id = hit_id
        et.save()

