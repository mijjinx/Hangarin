from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, SubTask, Category, Priority
from .forms import TaskForm, SubTaskForm, CategoryForm, PriorityForm

@login_required
def task_list(request):
    tasks = Task.objects.prefetch_related('subtasks', 'notes').select_related('category', 'priority').all()
    return render(request, 'task/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create New Task', 'back_url': 'task_list'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Task', 'back_url': 'task_list'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': task.title, 'back_url': 'task_list'})

@login_required
def subtask_list(request):
    subtasks = SubTask.objects.select_related('parent_task').all()
    return render(request, 'task/subtask_list.html', {'subtasks': subtasks})

@login_required
def subtask_create(request):
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subtask_list')
    else:
        form = SubTaskForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create SubTask', 'back_url': 'subtask_list'})

@login_required
def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('subtask_list')
    else:
        form = SubTaskForm(instance=subtask)
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit SubTask', 'back_url': 'subtask_list'})

@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        subtask.delete()
        return redirect('subtask_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': subtask.title, 'back_url': 'subtask_list'})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'task/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create Category', 'back_url': 'category_list'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Category', 'back_url': 'category_list'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': category.name, 'back_url': 'category_list'})

@login_required
def priority_list(request):
    priorities = Priority.objects.all()
    return render(request, 'task/priority_list.html', {'priorities': priorities})

@login_required
def priority_create(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create Priority', 'back_url': 'priority_list'})

@login_required
def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm(instance=priority)
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Priority', 'back_url': 'priority_list'})

@login_required
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('priority_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': priority.name, 'back_url': 'priority_list'})