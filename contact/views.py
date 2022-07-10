from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from . import forms


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('user:registration')

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

    @classmethod
    def as_views(cls):
        pass


def contact_view(request):
    form = forms.ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            sender = form.cleaned_data.get('sender')

            send_mail(subject, message, sender, ["a@a.pl"])
            return redirect(reverse_lazy("user:registration"))

    return render(request, 'contact/contact.html', {'form': form})
