from hangarin_project.task.models import Note
from hangarin_project.task.models import Category
from hangarin_project.task.models import Priority
from hangarin_project.task.models import SubTask
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", "priority", "category")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task_name')
    list_filter = ("status")
    search_fields = ("title")


@admin.display(description='Parent Task')
def parent_task_name(self, obj):
    return obj.parent_task.title

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

