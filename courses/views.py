from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateResponseMixin, View

from . import models
from .forms import ModuleFormset
from .permissions import AuthorManageMixin


class CoursesView(ListView):
    model = models.Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'


class CoruseDetailView(DetailView):
    model = models.Course
    template_name = 'courses/courses_page.html'
    context_object_name = 'course'


class CreateCourseView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Course
    fields = ('title', 'subject', 'slug', 'overview', 'course_image')
    template_name = 'courses/create_course.html'
    login_url = reverse_lazy('user:login')
    success_url = reverse_lazy('courses:courses')
    permission_required = 'courses.add_course'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, AuthorManageMixin, DeleteView):
    model = models.Course
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy('courses:courses')
    permission_required = 'courses.delete_course'
    login_url = reverse_lazy('user:login')
    context_object_name = 'course'


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, AuthorManageMixin, UpdateView):
    model = models.Course
    fields = ('title', 'subject', 'slug', 'overview', 'course_image')
    template_name = 'courses/update_course.html'
    success_url = reverse_lazy('courses:courses')
    permission_required = 'courses.change_course'
    login_url = reverse_lazy('user:login')
    context_object_name = 'course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/add_module_course.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # self.course = models.Course.objects.filter(pk=pk, owner=request.user)
        self.course = get_object_or_404(models.Course, pk=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('courses:courses'))
        return self.render_to_response({'course': self.course, 'formset': formset})


@login_required
def student_enrollment(request, course_slug):
    if request.method == 'POST':
        try:
            course = models.Course.objects.get(slug=course_slug)
            if course is not None:
                students = course.students.all()
                if request.user not in students:
                    course.students.add(request.user)
                    messages.add_message(request, messages.SUCCESS, f'You enrolled in {course.title} course!')
                    return redirect(reverse_lazy('courses:courses'))
                else:
                    messages.add_message(request, messages.WARNING, 'You already in this course!')
                    return redirect(reverse_lazy('courses:courses'))
            else:
                messages.add_message(request, messages.WARNING, 'Course does not exist!')
                return redirect(reverse_lazy('courses:courses'))
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Course not found!')
            return redirect(reverse_lazy('courses:courses'))


class StudentCourseDetailView(DetailView):
    model = models.Course
    template_name = 'courses/course_student_view.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.first()

        return context
