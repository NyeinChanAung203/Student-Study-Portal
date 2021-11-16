from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('note',kwargs={'pk':self.pk})



class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return f"{self.subject}-{self.title}"
    
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'