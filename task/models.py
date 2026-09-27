from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    class Meta:
        abstract = True

class Priority(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default="Pending")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name = "priority_tasks")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = "category_tasks")

    def __str__(self):
        return self.title
    
class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"

class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    parent_task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name ='subtasks')
    title = models.CharField(max_length = 255) 
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default = "Pending")

    def __str__(self):
        return self.title

    

    