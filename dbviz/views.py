from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from coursework.settings import MEDIA_URL
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
import torch
import torchvision
from torchvision import transforms as T
from datetime import datetime

def index(request):
    if request.method == 'GET':
        return render(request, 'dbviz/index.html')
    return  JsonResponse({'errors': ''}, status=400)

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = EmployeeForm()
    return render(request, 'dbviz/employee_create.html', {'form': form})

def employees(request):
    if request.method == 'GET':
        employs = Employee.objects.all()
        return render(request, 'dbviz/employees.html', {'employees': employs, 'MEDIA_URL': MEDIA_URL})
    return  JsonResponse({'errors': ''}, status=400)
def employee_delete(request, id):
    if request.method == 'POST':
        empl = Employee.objects.get(empl_id=id)
        tasks = Task.objects.all()
        for task in tasks:
            if empl in task.employee.all():
                return redirect(request.META.get('HTTP_REFERER'))
        empl.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)


def construction_site_create(request):
    if request.method == 'POST':
        form = ConstructionSiteForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = ConstructionSiteForm()
    return render(request, 'dbviz/construction_site_create.html', {'form': form})
def construction_sites(request):
    if request.method == 'GET':
        const_sites = ConstructionSite.objects.all()
        tasks = Task.objects.all()
        return render(request, 'dbviz/construction_sites.html', {'const_sites': const_sites, 'tasks': tasks, 'MEDIA_URL': MEDIA_URL})
    return  JsonResponse({'errors': ''}, status=400)
def construction_site_delete(request, id):
    if request.method == 'POST':
        
        ConstructionSite.objects.filter(const_site_id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)

def construction_tools_create(request):
    if request.method == 'POST':
        form = ConstructionToolsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = ConstructionToolsForm()
    return render(request, 'dbviz/construction_tools_create.html', {'form': form})
def construction_tools(request):
    if request.method == 'GET':
        const_tools = ConstructionTools.objects.all()
        return render(request, 'dbviz/construction_tools.html', {'const_tools': const_tools, 'MEDIA_URL': MEDIA_URL})
    return  JsonResponse({'errors': ''}, status=400)
def  construction_tools_delete(request, id):
    if request.method == 'POST':
        tools = ConstructionTools.objects.get(const_tools_id=id)
        tasks = Task.objects.all()
        for task in tasks:
            if tools in task.const_tools.all():
                return redirect(request.META.get('HTTP_REFERER'))
        tools.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'dbviz/task_create.html', {'form': form})
def tasks(request):
    if request.method == 'GET':
        taskss = Task.objects.all()
        return render(request, 'dbviz/tasks.html', {'tasks': taskss, 'MEDIA_URL': MEDIA_URL})
    return  JsonResponse({'errors': ''}, status=400)
def task_delete(request, id):
    if request.method == 'POST':
        Task.objects.filter(task_id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)

def model_create(request):
    if request.method == 'POST':
        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = ModelForm()
    return render(request, 'dbviz/model_create.html', {'form': form})
def model_s(request):
    if request.method == 'GET':
        modelss = Model.objects.all()
        return render(request, 'dbviz/models.html', {'models': modelss, 'MEDIA_URL': MEDIA_URL})
    return  JsonResponse({'errors': ''}, status=400)
def  model_delete(request, id):
    if request.method == 'POST':
        Model.objects.filter(model_id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)


def report_delete(request, id):
    if request.method == 'POST':
        Report.objects.get(report_id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'errors': ''}, status=400)



def task_view(request, id):
    if request.method == 'GET':
        task = Task.objects.get(task_id=id)
        tools = task.const_tools.all()
        employees = task.employee.all()
        reports = Report.objects.filter(task=id)
        return render(request, 'dbviz/task.html', {'task': task, 'tools': tools, 'employees': employees, 'reports': reports})
    return JsonResponse({'errors': ''}, status=400)
def employee_view(request, id):
    if request.method == 'GET':
        empl = Employee.objects.get(empl_id=id)
        dates = WorkingDay.objects.all()
        days = []
        for date in dates:
            if date.empl.filter(empl_id=id).exists():
                days.append( date)
        return render(request, 'dbviz/employee.html', {'employee': empl, 'days': days})
    return JsonResponse({'errors': ''}, status=400)
def report_view(request, id):
    report = Report.objects.get(report_id=id)
    return render(request, 'dbviz/report.html', {'report': report, 'tools': report.const_tools.all()})

class PostWorkDay(APIView):
    def post(self, request):
        data = request.POST.dict()
        empl_ip = int(data['empl_id'])
        empl = Employee.objects.filter(empl_id=empl_ip).first()
        if not empl:
            return JsonResponse({'errors': 'The employee does not exist'}, status=400)
        date = WorkingDay.objects.filter(working_day_date=data['date']).first()
        if date and not empl in date.empl.all():
            print(date)
            date = date.empl.add(empl)
            return JsonResponse({}, status=200)
        elif not date:
            WorkingDay.objects.create(working_day_date=data['date']).empl.set([empl])
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({'errors': 'The employee has already been recorded'}, status=400)
class GenReport(APIView):
    def post(self, request):
        data = request.POST.dict()
        model_id = int(data['model_id'])
        task_id = int(data['task_id'])
        file = request.FILES['image']
        model_obj = Model.objects.filter(model_id=model_id).first()
        task = Task.objects.filter(task_id=task_id).first()
        if not task:
            return JsonResponse({'errors': 'Task does not exist'}, status=400)
        if not model_obj:
            return JsonResponse({'errors': 'Model does not exist'}, status=400)
        model = torch.load(os.path.join(MEDIA_ROOT, str(model_obj.path.path)), map_location=torch.device('cpu'))
        img = T.ToTensor()(Image.open(file).convert("RGB"))
        model.eval()
        device = torch.device('cpu')
        with torch.no_grad():
            prediction = model([img.to(device)])
        labels = prediction[0]['labels']
        trash = []
        people_counter = 0
        tools = []
        for id in labels:
            if id == 1:
                people_counter+=1
            elif not id in trash:
                tool = ConstructionTools.objects.filter(code=id).first()
                if tool:
                    tools.append(tool)
                trash.append(id)
        Report.objects.create(task=task, model=model_obj, report_time=str(datetime.now()),
                              original_image=file,
                               people_num=people_counter).const_tools.set(tools)
        return JsonResponse({}, status=200)
        