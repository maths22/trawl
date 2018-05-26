from django import forms

class SubmitTemplate(forms.Form):
    worker_id = forms.HiddenInput()
    message_template = forms.CharField(label='Message template', max_length=100)
