from django.urls import path

from data_consumption.views import UploadAndSaveView, GraphView, BuildingsView, MeterView, MeterHourlyView

urlpatterns = [
    path("", UploadAndSaveView.as_view()),
    path("buildings/", BuildingsView.as_view()),
    path("list_buildings/<int:pk>/meters/", MeterView.as_view()),
    path("list_buildings/<int:pk>/meters/<int:meter_id>/list_half_hourly_data/", MeterHourlyView.as_view()),
    path("meter/<int:pk>/show_graph/", GraphView.as_view())
]
