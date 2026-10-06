from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task, SubTask, Category, Priority, Note
from .forms import TaskForm, SubTaskForm, CategoryForm, PriorityForm, NoteForm

def pwa_manifest_custom(request):
    manifest_data = {
        "id": "/",
        "name": "Hangarin",
        "short_name": "Hangarin",
        "description": "A Progressive Web App version of Hangarin",
        "start_url": "/accounts/login/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#ECFEFF",
        "theme_color": "#164E63",
        "prefer_related_applications": False,
        "icons": [
            {
                "src": "/static/img/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/img/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/img/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "maskable"
            },
            {
                "src": "/static/img/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            }
        ]
    }
    return JsonResponse(manifest_data)

@login_required
def home(request):
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status='Pending').count()
    completed_tasks = Task.objects.filter(status='Completed').count()
    categories_count = Category.objects.count()
    
    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'categories_count': categories_count,
        'active_tab': 'home'
    }
    return render(request, 'task/home.html', context)

from django.db.models import Q

@login_required
def task_list(request):
    tasks = Task.objects.prefetch_related('subtasks', 'notes').select_related('category', 'priority').all()
    
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'deadline_asc')

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if sort_by == 'deadline_asc':
        tasks = tasks.order_by('deadline')
    elif sort_by == 'deadline_desc':
        tasks = tasks.order_by('-deadline')
    elif sort_by == 'title_asc':
        tasks = tasks.order_by('title')
    elif sort_by == 'title_desc':
        tasks = tasks.order_by('-title')
    elif sort_by == 'priority':
        tasks = tasks.order_by('priority__name')
    elif sort_by == 'created_at':
        tasks = tasks.order_by('-created_at')

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'sort_by': sort_by,
        'active_tab': 'tasks'
    }
    return render(request, 'task/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create New Task', 'back_url': 'task_list', 'active_tab': 'tasks'})

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
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Task', 'back_url': 'task_list', 'active_tab': 'tasks'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': task.title, 'back_url': 'task_list', 'active_tab': 'tasks'})

@login_required
def subtask_list(request):
    subtasks = SubTask.objects.select_related('parent_task').all()
    
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'recent')

    if search_query:
        subtasks = subtasks.filter(Q(title__icontains=search_query) | Q(parent_task__title__icontains=search_query))

    if sort_by == 'recent':
        subtasks = subtasks.order_by('-created_at')
    elif sort_by == 'oldest':
        subtasks = subtasks.order_by('created_at')
    elif sort_by == 'title_asc':
        subtasks = subtasks.order_by('title')
    elif sort_by == 'title_desc':
        subtasks = subtasks.order_by('-title')
    elif sort_by == 'status':
        subtasks = subtasks.order_by('status')
    elif sort_by == 'parent_task':
        subtasks = subtasks.order_by('parent_task__title')

    context = {
        'subtasks': subtasks,
        'search_query': search_query,
        'sort_by': sort_by,
        'active_tab': 'subtasks'
    }
    return render(request, 'task/subtask_list.html', context)

@login_required
def subtask_create(request):
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subtask_list')
    else:
        form = SubTaskForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create SubTask', 'back_url': 'subtask_list', 'active_tab': 'subtasks'})

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
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit SubTask', 'back_url': 'subtask_list', 'active_tab': 'subtasks'})

@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        subtask.delete()
        return redirect('subtask_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': subtask.title, 'back_url': 'subtask_list', 'active_tab': 'subtasks'})

@login_required
def note_list(request):
    notes = Note.objects.select_related('task').all()

    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'recent')

    if search_query:
        notes = notes.filter(Q(content__icontains=search_query) | Q(task__title__icontains=search_query))

    if sort_by == 'recent':
        notes = notes.order_by('-created_at')
    elif sort_by == 'oldest':
        notes = notes.order_by('created_at')
    elif sort_by == 'task':
        notes = notes.order_by('task__title')

    context = {
        'notes': notes,
        'search_query': search_query,
        'sort_by': sort_by,
        'active_tab': 'notes'
    }
    return render(request, 'task/note_list.html', context)

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create Note', 'back_url': 'note_list', 'active_tab': 'notes'})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Note', 'back_url': 'note_list', 'active_tab': 'notes'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': f"Note for {note.task.title}", 'back_url': 'note_list', 'active_tab': 'notes'})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'task/category_list.html', {'categories': categories, 'active_tab': 'categories'})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create Category', 'back_url': 'category_list', 'active_tab': 'categories'})

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
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Category', 'back_url': 'category_list', 'active_tab': 'categories'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': category.name, 'back_url': 'category_list', 'active_tab': 'categories'})

@login_required
def priority_list(request):
    priorities = Priority.objects.all()
    return render(request, 'task/priority_list.html', {'priorities': priorities, 'active_tab': 'priorities'})

@login_required
def priority_create(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Create Priority', 'back_url': 'priority_list', 'active_tab': 'priorities'})

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
    return render(request, 'task/generic_form.html', {'form': form, 'title': 'Edit Priority', 'back_url': 'priority_list', 'active_tab': 'priorities'})

@login_required
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('priority_list')
    return render(request, 'task/generic_confirm_delete.html', {'item_name': priority.name, 'back_url': 'priority_list', 'active_tab': 'priorities'})