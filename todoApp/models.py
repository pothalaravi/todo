from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('entertainment', 'Entertainment'),
        ('fitness', 'Fitness'),
        ('others', 'Others'),
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=200,null=True)
    description=models.TextField(null=True,blank=True)
    task_date = models.DateTimeField(null=True)
    category = models.CharField(max_length=20, default="others", choices=CATEGORY_CHOICES)
    completed=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['completed']
