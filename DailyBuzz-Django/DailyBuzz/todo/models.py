from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    to_be_completed = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)
    def save(self, *args, **kwargs):
        # If completed is set to True and no completion_time is set
        if self.completed and self.completion_time is None:
            self.completion_time = timezone.now()
        
        # Optional: Clear completion_time if marked incomplete
        elif not self.completed:
            self.completion_time = None

        super().save(*args, **kwargs)