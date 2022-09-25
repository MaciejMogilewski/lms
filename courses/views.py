from django.shortcuts import render
from django.views.generic import ListView, DetailView

from . import models


class CoursesView(ListView):
    model = models.Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'


class CoruseDetailView(DetailView):
    model = models.Course
    template_name = 'courses/courses_page.html'
    context_object_name = 'course'
