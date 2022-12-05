from django import forms


class MeterForm(forms.Form):
    meter_csv_file = forms.FileField()


class HalfHourlyForm(forms.Form):
    half_hour_csv_file = forms.FileField()


class BuildingForm(forms.Form):
    building_csv_file = forms.FileField()
