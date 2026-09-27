from hangarin_project.task.models import Reminder
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from task.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = "Populates the database with default Priority, Category, and fake Tasks, Notes, and SubTasks"
    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write("Seeding Priorities and Categories...")

        # Priority recods 
        priority_list = ['high','medium','low','critical','optional']
        priority_obj = []
        for prio in priority_list:
            priority, created = Priority.objects.get_or_create(name=prio)
            priority_obj.append(priority)

        # Category records 
        category_list = ['work','school','personal','health','finance','social','shopping','other']
        category_obj = []
        for cat in category_list:
            category, created = Category.objects.get_or_create(name=cat)
            category_obj.append(category)
        
        status_choices = ["Pending", "In progress", "Completed"]

        self.stdout.write("Generating fake Tasks, Notes, and SubTasks...")

        # 15 fake task
        for _ in range(15):

           task_title = fake.sentence(nb_words = 5)
           task_description = fake.paragraph(nb_sentences = 3) 
           task_status = fake.random_element(elements=status_choices)
           naive_date = fake.date_time_month()
           aware_deadline = timezone.make_aware(naive_date)

           task_obj = Task.objects.create(
            title = task_title,
            description = task_description,
            status = task_status,
            due_date = aware_deadline,
            priority = fake.random_element(elements = priority_obj),
            category = fake.random_element(elements = category_obj)
           )

           for _ in range(random.randint(1, 4)):
            SubTask.objects.create(
                parent_task=task_obj,
                title=fake.sentence(nb_words=4),
                status=fake.random_element(elements=status_choices)
            )
            
            for _ in range(random.randint(1, 2)):
                Note.objects.create(
                    task=task_obj,
                    content=fake.sentence(nb_words=2)
                )

            Reminder.objects.create(
                task=task_obj,
                remind_at=aware_deadline - timezone.timedelta(hours=2)
            )    
                
        self.stdout.write(self.style.SUCCESS("Database successfully populated with seed data!"))
