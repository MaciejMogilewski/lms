from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

    def send_mail(self):
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')
        sender = self.cleaned_data.get('sender')

        send_mail(subject, message, sender, ["a@a.pl"])