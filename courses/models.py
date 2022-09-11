from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from courses.fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='courses_creator')
    title = models.CharField(max_length=200)
    subject = models.ForeignKey('Subject', related_name='courses', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(get_user_model(), related_name='courses_students', blank=True)
    course_image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='modules')
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']
