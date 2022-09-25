from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from . import models
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




