from django.db import models
from django.contrib.auth.models import User
from coursework.settings import BASE_DIR
import os


class Employee(models.Model):
    empl_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    empl_date = models.DateField()
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    post = models.CharField(max_length=250)
    photo = models.ImageField(upload_to="media/db")
    gender = models.BooleanField()
    birth_date = models.DateField()
    citizenship = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return f"{self.last_name} {self.name}"
class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    path = models.ImageField(upload_to="media/db")
    description = models.TextField(max_length=350)
    creation_date = models.DateTimeField()
    empl = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class WorkingDay(models.Model):
    working_day_id = models.AutoField(primary_key=True)
    working_day_date = models.DateField()
    empl = models.ManyToManyField(User)
    def __str__(self):
        return f"День {str(self.working_day_date)}"
class ConstructionSite(models.Model):
    const_site_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250)
    name = models.CharField(max_length=150)
    const_start_date = models.DateField()
    const_compl_date = models.DateField()
    def __str__(self):
        return self.name
class ConstructionTools(models.Model):
    const_tools_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    code = models.IntegerField()
    def __str__(self):
        return self.name
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=350)
    start_date = models.DateField()
    compl_date = models.DateField()
    const_site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    const_tools = models.ManyToManyField(ConstructionTools, blank=True, null=True)
    employee = models.ManyToManyField(Employee)
    def __str__(self):
        return f"Задача №{str(self.task_id)}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    original_image = models.ImageField(upload_to="media/db")
    processed_image = models.ImageField(upload_to="media/db")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    report_time = models.TimeField()
    people_num = models.IntegerField()
    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    const_tools = models.ManyToManyField(ConstructionTools)
    def __str__(self):
        return f"Отчет №{str(self.report_id)}"