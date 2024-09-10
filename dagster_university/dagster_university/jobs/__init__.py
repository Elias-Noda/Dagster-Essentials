from dagster import AssetSelection
from dagster import AssetSelection, define_asset_job
from dagster import ScheduleDefinition
from ..jobs import trip_update_job
from ..partitions import monthly_partition
from ..partitions import weekly_partition

adhoc_request = AssetSelection.assets(["adhoc_request"])

trips_by_week = AssetSelection.assets("trips_by_week")


trip_update_job = define_asset_job(
    name="trip_update_job",
    partitions_def=monthly_partition,
    selection=AssetSelection.all() - trips_by_week - adhoc_request
)


weekly_update_job = define_asset_job(
    name="weekly_update_job",
    partitions_def=weekly_partition,
    selection=trips_by_week,
)

trip_update_schedule = ScheduleDefinition(
    job=trip_update_job,
    cron_schedule="0 0 5 * *", # every 5th of the month at midnight
)

adhoc_request_job = define_asset_job(
    name="adhoc_request_job",
    selection=adhoc_request,
)