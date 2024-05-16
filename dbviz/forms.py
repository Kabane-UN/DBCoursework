from django import forms
from .models import *
from django.forms import widgets

birth_years = ('1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005')
empl_years = ('2010', '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023')
class EmployeeForm(forms.ModelForm):
    empl_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    birth_date = forms.DateField(widget=widgets.SelectDateWidget(years=birth_years))
    class Meta:
        model = Employee
        fields = ('name','last_name','patronymic', 'empl_date', 'salary', 'post', 'photo', 'gender', 'birth_date', 'citizenship', 'user')
class ConstructionSiteForm(forms.ModelForm):
    const_start_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    const_compl_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    class Meta:
        model = ConstructionSite
        fields = ('address', 'name', 'const_start_date', 'const_compl_date')
class ConstructionToolsForm(forms.ModelForm):
    class Meta:
        model = ConstructionTools
        fields = ('name', 'code')
class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    compl_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    class Meta:
        model = Task
        fields = ('description', 'start_date', 'compl_date','const_site','const_tools','employee')
class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ('name' ,'path' ,'description', 'empl')
