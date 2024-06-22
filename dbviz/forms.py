from django import forms
from .models import *
from django.forms import widgets

birth_years = tuple((str(i) for i in range(1900, 2999)))
empl_years = tuple((str(i) for i in range(2024, 2999)))


class EmployeeForm(forms.ModelForm):
    empl_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    birth_date = forms.DateField(widget=widgets.SelectDateWidget(years=birth_years))

    class Meta:
        model = Employee
        fields = (
            "name",
            "last_name",
            "patronymic",
            "empl_date",
            "salary",
            "post",
            "photo",
            "gender",
            "birth_date",
            "citizenship",
            "user",
        )


class ConstructionSiteForm(forms.ModelForm):
    const_start_date = forms.DateField(
        widget=widgets.SelectDateWidget(years=empl_years)
    )
    const_compl_date = forms.DateField(
        widget=widgets.SelectDateWidget(years=empl_years)
    )

    class Meta:
        model = ConstructionSite
        fields = ("address", "name", "const_start_date", "const_compl_date")


class ConstructionToolsForm(forms.ModelForm):
    class Meta:
        model = ConstructionTools
        fields = ("name", "code")


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))
    compl_date = forms.DateField(widget=widgets.SelectDateWidget(years=empl_years))

    class Meta:
        model = Task
        fields = (
            "description",
            "start_date",
            "compl_date",
            "const_site",
            "const_tools",
            "employee",
        )


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ("name", "path", "description", "empl")


class CitizenshipForm(forms.ModelForm):
    class Meta:
        model = Citizenship
        fields = ("name",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("name",)
