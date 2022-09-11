from django.contrib import admin

from . import models

admin.site.register(models.Image)
admin.site.register(models.Video)
admin.site.register(models.Text)
admin.site.register(models.File)
admin.site.register(models.Content)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ModuleInLine(admin.StackedInline):
    model = models.Module


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created')
    list_filter = ('created', 'subject')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ModuleInLine, )
