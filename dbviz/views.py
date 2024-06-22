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
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.method == "GET":
        return render(request, "dbviz/index.html")
    return JsonResponse({"errors": ""}, status=400)


@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = EmployeeForm()
    return render(request, "dbviz/employee/create.html", {"form": form})


@login_required
def employee_update(request, id):
    empl = Employee.objects.get(pk=id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=empl)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:

        form = EmployeeForm(None, None, instance=empl)
    return render(request, "dbviz/employee/update.html", {"form": form})


@login_required
def employees(request):
    if request.method == "GET":
        employs = Employee.objects.all()
        return render(
            request,
            "dbviz/employee/view_all.html",
            {"employees": employs, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def employee_delete(request, id):
    if request.method == "POST":
        empl = Employee.objects.get(pk=id)
        if Task.objects.filter(employee__pk=id).exists():
            return redirect(request.META.get("HTTP_REFERER"))
        empl.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def construction_site_create(request):
    if request.method == "POST":
        form = ConstructionSiteForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = ConstructionSiteForm()
    return render(request, "dbviz/construction_site/create.html", {"form": form})


@login_required
def construction_site_update(request, id):
    construction_site = ConstructionSite.objects.get(const_site_id=id)
    if request.method == "POST":
        form = ConstructionSiteForm(request.POST, instance=construction_site)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:

        form = ConstructionSiteForm(None, instance=construction_site)
    return render(request, "dbviz/construction_site/update.html", {"form": form})


@login_required
def construction_sites(request):
    if request.method == "GET":
        const_sites = ConstructionSite.objects.all()
        tasks = [
            Task.objects.filter(const_site__pk=i.const_site_id) for i in const_sites
        ]
        const_sites_and_tasks = zip(const_sites, tasks)
        return render(
            request,
            "dbviz/construction_site/view_all.html",
            {"const_sites_and_tasks": const_sites_and_tasks, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def construction_site_delete(request, id):
    if request.method == "POST":

        ConstructionSite.objects.filter(const_site_id=id).delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def construction_tools_create(request):
    if request.method == "POST":
        form = ConstructionToolsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = ConstructionToolsForm()
    return render(request, "dbviz/construction_tools/create.html", {"form": form})


@login_required
def construction_tools_update(request, id):
    conts_tools = ConstructionTools.objects.get(const_tools_id=id)
    if request.method == "POST":
        form = ConstructionToolsForm(request.POST, instance=conts_tools)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:

        form = TaskForm(None, instance=conts_tools)
    return render(request, "dbviz/construction_tools/update.html", {"form": form})


@login_required
def construction_tools(request):
    if request.method == "GET":
        const_tools = ConstructionTools.objects.all()
        return render(
            request,
            "dbviz/construction_tools/view_all.html",
            {"const_tools": const_tools, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def construction_tools_delete(request, id):
    if request.method == "POST":
        tools = ConstructionTools.objects.get(const_tools_id=id)
        if Task.objects.filter(const_tools__pk=id).exists():
            return redirect(request.META.get("HTTP_REFERER"))
        tools.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = TaskForm()
    return render(request, "dbviz/task/create.html", {"form": form})


@login_required
def task_update(request, id):
    task = Task.objects.get(pk=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = TaskForm(None, instance=task)
    return render(request, "dbviz/task/update.html", {"form": form})


@login_required
def tasks(request):
    if request.method == "GET":
        taskss = Task.objects.all()
        return render(
            request,
            "dbviz/task/view_all.html",
            {"tasks": taskss, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def task_delete(request, id):
    if request.method == "POST":
        Task.objects.filter(pk=id).delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def model_create(request):
    if request.method == "POST":
        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = ModelForm()
    return render(request, "dbviz/model/create.html", {"form": form})


@login_required
def model_update(request, id):
    model = Model.objects.get(pk=id)
    if request.method == "POST":
        form = ModelForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:

        form = ModelForm(None, None, instance=model)
    return render(request, "dbviz/model/update.html", {"form": form})


@login_required
def model_s(request):
    if request.method == "GET":
        modelss = Model.objects.all()
        return render(
            request,
            "dbviz/model/view_all.html",
            {"models": modelss, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def model_delete(request, id):
    if request.method == "POST":
        Model.objects.filter(pk=id).delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def report_delete(request, id):
    if request.method == "POST":
        Report.objects.get(pk=id).delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def citizenship_create(request):
    if request.method == "POST":
        form = CitizenshipForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = CitizenshipForm()
    return render(request, "dbviz/citizenship/create.html", {"form": form})


@login_required
def citizenship_update(request, id):
    citizenship = Citizenship.objects.get(citizenship_id=id)
    if request.method == "POST":
        form = CitizenshipForm(request.POST, instance=citizenship)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:

        form = CitizenshipForm(None, instance=citizenship)
    return render(request, "dbviz/citizenship/update.html", {"form": form})


@login_required
def citizenships(request):
    if request.method == "GET":
        citizenships = Citizenship.objects.all()
        return render(
            request,
            "dbviz/citizenship/view_all.html",
            {"citizenships": citizenships, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def citizenship_delete(request, id):
    if request.method == "POST":
        citizenship = Citizenship.objects.get(citizenship_id=id)
        if Employee.objects.filter(citizenship=id).exists():
            return redirect(request.META.get("HTTP_REFERER"))
        citizenship.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = PostForm()
    return render(request, "dbviz/post/create.html", {"form": form})


@login_required
def post_update(request, id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:

        form = PostForm(None, instance=post)
    return render(request, "dbviz/post/update.html", {"form": form})


@login_required
def posts(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(
            request,
            "dbviz/post/view_all.html",
            {"posts": posts, "MEDIA_URL": MEDIA_URL},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def post_delete(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)
        if Employee.objects.filter(post=id).exists():

            return redirect(request.META.get("HTTP_REFERER"))
        post.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return JsonResponse({"errors": ""}, status=400)


@login_required
def task_view(request, id):
    if request.method == "GET":
        task = Task.objects.get(pk=id)
        tools = task.const_tools.all()
        employees = task.employee.all()
        reports = Report.objects.filter(task=id)
        return render(
            request,
            "dbviz/task/view.html",
            {"task": task, "tools": tools, "employees": employees, "reports": reports},
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def employee_view(request, id):
    if request.method == "GET":
        empl = Employee.objects.get(pk=id)
        dates = WorkingDay.objects.filter(empl__pk=id)
        return render(
            request, "dbviz/employee/view.html", {"employee": empl, "days": dates}
        )
    return JsonResponse({"errors": ""}, status=400)


@login_required
def report_view(request, id):
    report = Report.objects.get(report_id=id)
    return render(
        request,
        "dbviz/report/view.html",
        {"report": report, "tools": report.const_tools.all()},
    )


class PostWorkDay(APIView):
    def post(self, request):
        data = request.POST.dict()
        empl_ip = int(data["empl_id"])
        empl = Employee.objects.filter(pk=empl_ip).first()
        input_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        WorkingDay.objects.filter(
            working_day_date__lte=input_date - timedelta(days=input_date.day)
        ).delete()
        if not empl:
            return JsonResponse({"errors": "The employee does not exist"}, status=400)
        dates = WorkingDay.objects.filter(working_day_date=data["date"])
        if dates.exists() and not dates.filter(empl__pk=empl_ip).exists():
            date = dates.get(working_day_date=data["date"])
            date.empl.add(empl)
            return JsonResponse({}, status=200)
        elif not dates.exists():
            WorkingDay.objects.create(working_day_date=data["date"]).empl.set([empl])
            return JsonResponse({}, status=200)
        return JsonResponse(
            {"errors": "The employee has already been recorded"}, status=400
        )


class GenReport(APIView):
    def post(self, request):
        data = request.POST.dict()
        model_id = int(data["model_id"])
        task_id = int(data["task_id"])
        file = request.FILES["image"]
        model_obj = Model.objects.filter(pk=model_id).first()
        task = Task.objects.filter(pk=task_id).first()
        if not task:
            return JsonResponse({"errors": "Task does not exist"}, status=400)
        if not model_obj:
            return JsonResponse({"errors": "Model does not exist"}, status=400)
        model = torch.load(
            os.path.join(MEDIA_ROOT, str(model_obj.path.path)),
            map_location=torch.device("cpu"),
        )
        img = T.ToTensor()(Image.open(file).convert("RGB"))
        model.eval()
        device = torch.device("cpu")
        with torch.no_grad():
            prediction = model([img.to(device)])
        labels = prediction[0]["labels"]
        people_counter = 0
        tools_id = set()
        for id in labels:
            if id == 1:
                people_counter += 1
            else:
                tools_id.add(id)
        tools = ConstructionTools.objects.filter(code__in=tools_id)
        Report.objects.create(
            task=task,
            model=model_obj,
            report_time=str(datetime.now()),
            original_image=file,
            people_num=people_counter,
        ).const_tools.set(tools)
        return JsonResponse({}, status=200)
