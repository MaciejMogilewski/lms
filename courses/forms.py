from django.forms import inlineformset_factory

from courses import models

ModuleFormset = inlineformset_factory(
    models.Course,
    models.Module,
    fields=('title', 'description'),
    extra=2,
    can_delete=True
)