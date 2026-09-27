from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.prefetch_related('subtasks', 'notes').select_related('category', 'priority').all()
    return render(request, 'task/task_list.html', {'tasks': tasks})