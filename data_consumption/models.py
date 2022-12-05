from django.db import models


class BuildingData(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "building_data"


class MeterData(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    fuel = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=20, null=True)
    building = models.ForeignKey(BuildingData, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "meter_data"


class HalfHourlyData(models.Model):
    consumption = models.FloatField(null=True)
    reading_date_time = models.DateTimeField()
    meter = models.ForeignKey(MeterData, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "half_hourly_data"

