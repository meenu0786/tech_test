import base64
import io
import urllib
from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from data_consumption.forms import MeterForm, HalfHourlyForm, BuildingForm
from data_consumption.models import BuildingData, MeterData, HalfHourlyData
from tech_test.celery_task.tasks import create_building_data, create_meter_data, \
    create_half_hourly_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class UploadAndSaveView(View):

    def get(self, request):
        return render(request, 'home.html', {'meter_form': MeterForm(), 'half_hourly_form': HalfHourlyForm(),
                                             'building_form': BuildingForm()})

    def post(self, request):
        building_form = BuildingForm(data=request.POST, files=request.FILES)
        if building_form.is_valid():
            df = pd.read_csv(building_form.cleaned_data.get("building_csv_file"))
            create_building_data.delay(len(df), df.to_json())
        meter_form = MeterForm(data=request.POST, files=request.FILES)
        if meter_form.is_valid():
            df = pd.read_csv(meter_form.cleaned_data.get("meter_csv_file"))
            create_meter_data.delay(len(df), df.to_json())
        half_hourly_form = HalfHourlyForm(data=request.POST, files=request.FILES)
        if half_hourly_form.is_valid():
            df = pd.read_csv(half_hourly_form.cleaned_data.get("half_hour_csv_file"))
            create_half_hourly_data.delay(len(df), df.to_json())
        return redirect("/buildings/")


class BuildingsView(ListView):
    model = BuildingData
    template_name = 'list_building.html'
    context_object_name = 'obj'


class MeterView(ListView):
    model = MeterData
    template_name = 'meter_list.html'
    context_object_name = 'obj'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(building__id=self.kwargs['pk'])


class MeterHourlyView(ListView):
    model = HalfHourlyData
    template_name = 'half_hourly.html'
    context_object_name = 'obj'

    def get_queryset(self):
        qs = super().get_queryset()
        meter=MeterData.objects.get(id=self.kwargs['meter_id'])
        return {"queryset": qs.filter(meter__id=self.kwargs['meter_id']), "meter_id": self.kwargs['meter_id'], "meter_unit": meter.unit}


class GraphView(View):

    def get(self, request, pk):
        days = []
        usage = []
        half_hourly_obj = HalfHourlyData.objects.filter(meter__id=pk).first()
        last_day = monthrange(half_hourly_obj.reading_date_time.year, half_hourly_obj.reading_date_time.month)[1]
        for day in range(1, last_day + 1):
            daily_usage = HalfHourlyData.objects.filter(meter__id=pk, reading_date_time__day=day).aggregate(
                daily_usage=Sum('consumption'))["daily_usage"]
            usage.append(daily_usage)
            days.append(day)
        plt.title(
            f"Usage For Month {['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'][half_hourly_obj.reading_date_time.month - 1]}")
        response = HttpResponse(content_type='image/png')
        data_plot = pd.DataFrame({"Days": days, "Usage": usage})
        sns.lineplot(x="Days", y="Usage", data=data_plot)
        plt.savefig(response, format='png')
        plt.clf()
        return response
