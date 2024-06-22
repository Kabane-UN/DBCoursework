from django.db import models
from django.contrib.auth.models import User
from coursework.settings import BASE_DIR, MEDIA_ROOT
import django.db.models.signals as signals
from django.dispatch import receiver
import os


class Citizenship(models.Model):
    citizenship_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"


class Employee(models.Model):
    empl_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    empl_date = models.DateField()
    salary = models.DecimalField(max_digits=11, decimal_places=2)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    photo = models.ImageField(upload_to="dbviz/employee")
    gender = models.BooleanField()
    birth_date = models.DateField()
    citizenship = models.ForeignKey(Citizenship, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.name}"


class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    path = models.FileField(upload_to="dbviz/model")
    description = models.TextField(max_length=350)
    creation_date = models.DateTimeField(auto_now=True)
    empl = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class WorkingDay(models.Model):
    working_day_id = models.AutoField(primary_key=True)
    working_day_date = models.DateField(unique=True)
    empl = models.ManyToManyField(Employee)

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
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=350)
    start_date = models.DateField()
    compl_date = models.DateField()
    const_site = models.ForeignKey(ConstructionSite, on_delete=models.DO_NOTHING)
    const_tools = models.ManyToManyField(ConstructionTools, blank=True)
    employee = models.ManyToManyField(Employee)

    def __str__(self):
        return f"Задача №{str(self.task_id)}"


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    original_image = models.ImageField(upload_to="dbviz/report")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    report_time = models.DateTimeField(auto_now=True)
    people_num = models.IntegerField()
    const_tools = models.ManyToManyField(ConstructionTools)

    def __str__(self):
        return f"Отчет №{str(self.report_id)}"


@receiver(signals.post_delete, sender=Employee)
def employee_post_delete_handler(sender, instance, **kwargs):
    path = os.path.join(MEDIA_ROOT, str(instance.photo.path))
    if os.path.isfile(path):
        os.remove(path)


@receiver(signals.pre_save, sender=Employee)
def employee_pre_update_handler(sender, instance, **kwargs):
    empl = sender.objects.filter(pk=instance.empl_id).first()
    if empl and instance.photo.path != empl.photo.path:
        path = os.path.join(MEDIA_ROOT, str(empl.photo.path))
        if os.path.isfile(path):
            os.remove(path)


@receiver(signals.post_delete, sender=Model)
def model_post_delete_handler(sender, instance, **kwargs):
    path = os.path.join(MEDIA_ROOT, str(instance.path.path))
    if os.path.isfile(path):
        os.remove(path)


@receiver(signals.pre_save, sender=Model)
def model_pre_update_handler(sender, instance, **kwargs):
    empl = sender.objects.filter(pk=instance.empl_id).first()
    if empl and instance.path.path != empl.path.path:
        path = os.path.join(MEDIA_ROOT, str(empl.path.path))
        if os.path.isfile(path):
            os.remove(path)


@receiver(signals.post_delete, sender=Report)
def report_post_delete_handler(sender, instance, **kwargs):
    path = os.path.join(MEDIA_ROOT, str(instance.original_image.path))
    if os.path.isfile(path):
        os.remove(path)
