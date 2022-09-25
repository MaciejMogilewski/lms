from django.contrib.auth.mixins import AccessMixin


class AuthorManageMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        item = self.get_queryset().filter(slug=kwargs.get('slug'))
        if not len(item) or request.user != item.first().owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)