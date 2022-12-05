import json

from celery import shared_task
from celery.utils.log import get_task_logger

from data_consumption.models import BuildingData, MeterData, HalfHourlyData

logger = get_task_logger(__name__)


@shared_task
def create_building_data(length, df):
    data = json.loads(df)
    building_data = [BuildingData(id=data.get("id").get(str(row)), name=data.get("name").get(str(row))) for row in
                     range(length)]
    BuildingData.objects.bulk_create(building_data)


@shared_task
def create_meter_data(length, df):
    data = json.loads(df)
    meter_data = []
    for row in range(length):
        try:
            mdo = MeterData(id=data.get("id").get(str(row)), fuel=data.get("fuel").get(str(row)),
                            unit=data.get("unit").get(str(row)),
                            building=BuildingData.objects.get(id=data.get("building_id").get(str(row))))
            meter_data.append(mdo)
        except BuildingData.DoesNotExist:
            continue
    MeterData.objects.bulk_create(meter_data)


@shared_task
def create_half_hourly_data(length, df):
    data = json.loads(df)
    half_hourly_objs = []
    for row in range(length):
        try:
            hho = HalfHourlyData(consumption=data.get("consumption").get(str(row)),
                                 reading_date_time=data.get("reading_date_time").get(str(row)),
                                 meter=MeterData.objects.get(id=data.get("meter_id").get(str(row))))
            half_hourly_objs.append(hho)
        except MeterData.DoesNotExist:
            continue
    HalfHourlyData.objects.bulk_create(half_hourly_objs)
