from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', index, name='index'),
    path('employee_create', employee_create, name='employee_create'),
    path('employees', employees, name='employees'),
    path('employee_delete/<int:id>/', employee_delete, name='employee_delete'),
    path('construction_site_create', construction_site_create, name='construction_site_create'),
    path('construction_sites', construction_sites, name='construction_sites'),
    path('construction_site_delete/<int:id>/', construction_site_delete, name='construction_site_delete'),

    path('construction_tools_create', construction_tools_create, name='construction_tools_create'),
    path('construction_tools', construction_tools, name='construction_tools'),
    path('construction_tools_delete/<int:id>/', construction_tools_delete, name='construction_tools_delete'),

    path('task_create', task_create, name='task_create'),
    path('tasks', tasks, name='tasks'),
    path('task_delete/<int:id>/', task_delete, name='task_delete'),

    path('model_create', model_create, name='model_create'),
    path('models', model_s, name='models'),
    path('model_delete/<int:id>/', model_delete, name='model_delete'),
    path('report_delete/<int:id>/', report_delete, name='report_delete'),
    path('task/<int:id>/', task_view, name='task'),
    path('employee/<int:id>/', employee_view, name='employee'),
    path('api/post_workday/', PostWorkDay.as_view(), name='api_post_workday'),
    path('api/gen_report/', GenReport.as_view(), name='api_gen_report'),
    path('report/<int:id>/', report_view, name='report'),
]
